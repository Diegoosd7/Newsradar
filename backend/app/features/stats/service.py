from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import (
    StatsResponse,
    StatsCreate,
    StatsUpdate,
    DashboardStatsResponse,
    DashboardSummary,
    CategoryCountItem,
    TrendingCategoryItem,
    TrendingWordItem,
)
from ...core.common_service import CommonService
from ...db.models import (
    Stats,
    Metric,
    CrossMetricStats,
    InformationSource,
    RSSChannel,
    NewsItem,
    Alert,
    AlertCategoryItem,
    CrossAlertAlertCategoryItem,
    Category,
)
import html
import re


class StatsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_stats(self) -> List[StatsResponse]:
        stats_list = self.db.query(Stats).all()
        return [self._to_response(stats) for stats in stats_list]

    def create_stats(self, payload: StatsCreate) -> StatsResponse:
        stats = Stats()
        self.db.add(stats)
        self.db.flush()

        self._replace_metrics(stats.id, payload.metrics)

        self.db.commit()
        self.db.refresh(stats)
        return self._to_response(stats)

    def get_stats(self, stats_id: int) -> StatsResponse:
        stats = self._get_stats_or_404(stats_id)
        return self._to_response(stats)

    def update_stats(self, stats_id: int, payload: StatsUpdate) -> StatsResponse:
        stats = self._get_stats_or_404(stats_id)
        data = payload.model_dump(exclude_unset=True)

        if "metrics" in data:
            self._replace_metrics(stats_id, data["metrics"])

        self.db.commit()
        self.db.refresh(stats)
        return self._to_response(stats)

    def delete_stats(self, stats_id: int) -> None:
        stats = self._get_stats_or_404(stats_id)
        (
            self.db.query(CrossMetricStats)
            .filter(CrossMetricStats.stats_id == stats_id)
            .delete(synchronize_session=False)
        )
        self.db.delete(stats)
        self.db.commit()

    def get_dashboard_stats(self) -> DashboardStatsResponse:
        summary = DashboardSummary(
            sources=self.db.query(InformationSource).count(),
            rss_channels=self.db.query(RSSChannel).count(),
            news=self.db.query(NewsItem).count(),
            alerts=self.db.query(Alert).count(),
        )

        news_by_category_rows = (
            self.db.query(Category.name, NewsItem.id)
            .join(RSSChannel, RSSChannel.category_id == Category.id)
            .join(NewsItem, NewsItem.channel_id == RSSChannel.id)
            .all()
        )

        news_counts: dict[str, int] = {}
        for category_name, _news_id in news_by_category_rows:
            news_counts[category_name] = news_counts.get(category_name, 0) + 1

        news_by_category = [
            CategoryCountItem(
                category_code=item["label"].upper().replace(" ", "_"),
                category_label=item["label"],
                count=item["count"],
            )
            for item in self._sorted_count_items(news_counts)
        ]

        alert_by_category_rows = (
            self.db.query(AlertCategoryItem.code, AlertCategoryItem.label)
            .join(
                CrossAlertAlertCategoryItem,
                CrossAlertAlertCategoryItem.alert_category_item_id == AlertCategoryItem.id,
            )
            .all()
        )

        alert_counts: dict[tuple[str, str], int] = {}
        for code, label in alert_by_category_rows:
            key = (code, label)
            alert_counts[key] = alert_counts.get(key, 0) + 1

        alerts_by_category = [
            CategoryCountItem(
                category_code=code,
                category_label=label,
                count=count,
            )
            for (code, label), count in sorted(
                alert_counts.items(),
                key=lambda item: (-item[1], item[0][1].lower()),
            )
        ]

        trending_by_category = self._build_trending_by_category()

        return DashboardStatsResponse(
            summary=summary,
            news_by_category=news_by_category,
            alerts_by_category=alerts_by_category,
            trending_by_category=trending_by_category,
        )

    def _get_stats_or_404(self, stats_id: int) -> Stats:
        stats = self.db.query(Stats).filter(Stats.id == stats_id).first()
        if stats is None:
            raise HTTPException(status_code=404, detail="Stats no encontrados")
        return stats

    def _replace_metrics(self, stats_id: int, metrics: List[dict]) -> None:
        (
            self.db.query(CrossMetricStats)
            .filter(CrossMetricStats.stats_id == stats_id)
            .delete(synchronize_session=False)
        )

        for metric_item in metrics:
            name = metric_item["name"] if isinstance(metric_item, dict) else metric_item.name
            value = metric_item["value"] if isinstance(metric_item, dict) else metric_item.value
            metric = Metric(name=name, value=value)
            self.db.add(metric)
            self.db.flush()
            self.db.add(CrossMetricStats(metric_id=metric.id, stats_id=stats_id))

    def _to_response(self, stats: Stats) -> StatsResponse:
        metrics = [
            {"name": name, "value": value}
            for name, value in (
                self.db.query(Metric.name, Metric.value)
                .join(CrossMetricStats, CrossMetricStats.metric_id == Metric.id)
                .filter(CrossMetricStats.stats_id == stats.id)
                .all()
            )
        ]
        return StatsResponse(id=stats.id, metrics=metrics)

    def _sorted_count_items(self, counts: dict[str, int]) -> list[dict]:
        return [
            {"label": label, "count": count}
            for label, count in sorted(
                counts.items(),
                key=lambda item: (-item[1], item[0].lower()),
            )
        ]

    def _build_trending_by_category(self) -> List[TrendingCategoryItem]:
        rows = (
            self.db.query(Category.name, NewsItem.title, NewsItem.summary)
            .join(RSSChannel, RSSChannel.category_id == Category.id)
            .join(NewsItem, NewsItem.channel_id == RSSChannel.id)
            .all()
        )

        stopwords = {
            "de", "la", "el", "en", "y", "a", "los", "las", "un", "una", "del",
            "por", "para", "con", "sin", "sobre", "tras", "ante", "entre",
            "desde", "hasta", "que", "se", "su", "sus", "al", "lo", "como",
            "más", "mas", "menos", "the", "and", "for", "from", "into", "this",
            "that", "uno", "es", "son", "ser", "ha", "han", "ya", "muy", "también",
            "tambien", "pero", "porque", "donde", "cuando", "quien", "quienes",
            "sobre", "tras", "cada", "entre", "según", "segun", "tras", "años",
            "ano", "años", "2024", "2025", "2026",
        }

        technical_noise = {
            "http", "https", "www", "com", "es", "html", "href", "target",
            "class", "width", "height", "rel", "src", "amp", "nbsp", "quot",
            "strong", "span", "div", "br", "img", "figure", "iframe", "self",
            "blank", "news", "feed", "rss",
            "aacute", "eacute", "iacute", "oacute", "uacute", "ntilde",
            "ldquo", "rdquo", "lsquo", "rsquo", "hellip", "mdash", "ndash",
        }

        category_words: dict[str, dict[str, int]] = {}

        for category_name, title, summary in rows:
            text = self._normalize_text_for_trending(title=title, summary=summary)
            words = self._tokenize(text)

            if category_name not in category_words:
                category_words[category_name] = {}

            for word in words:
                if len(word) < 4:
                    continue
                if word in stopwords or word in technical_noise:
                    continue
                if word.isdigit():
                    continue
                category_words[category_name][word] = (
                    category_words[category_name].get(word, 0) + 1
                )

        result: List[TrendingCategoryItem] = []
        for category_name, frequencies in sorted(
            category_words.items(),
            key=lambda item: item[0].lower(),
        ):
            top_words = sorted(
                frequencies.items(),
                key=lambda item: (-item[1], item[0]),
            )[:12]

            result.append(
                TrendingCategoryItem(
                    category_code=category_name.upper().replace(" ", "_"),
                    category_label=category_name,
                    words=[
                        TrendingWordItem(text=word, value=value)
                        for word, value in top_words
                    ],
                )
            )

        return result

    def _normalize_text_for_trending(self, title: str | None, summary: str | None) -> str:
        raw_text = f"{title or ''} {summary or ''}"

        # Decodifica entidades HTML como &aacute; -> á
        text = html.unescape(raw_text)

        # Elimina URLs completas
        text = re.sub(r"https?://\S+", " ", text)

        # Elimina etiquetas HTML
        text = re.sub(r"<[^>]+>", " ", text)

        # Elimina restos típicos de atributos HTML entrecomillados
        text = re.sub(r'["“”\'`´]+', " ", text)

        # Sustituye separadores raros por espacio
        text = re.sub(r"[/|_=:#]", " ", text)

        # Minúsculas
        text = text.lower()

        # Normaliza espacios
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def _tokenize(self, text: str) -> List[str]:
        cleaned = []
        current = []

        for char in text:
            if char.isalnum() or char in {"á", "é", "í", "ó", "ú", "ñ", "ü"}:
                current.append(char)
            else:
                if current:
                    cleaned.append("".join(current))
                    current = []

        if current:
            cleaned.append("".join(current))

        return cleaned