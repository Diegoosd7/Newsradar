from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import StatsResponse, StatsCreate, StatsUpdate
from ...core.common_service import CommonService
from ...db.models import Stats, Metric, CrossMetricStats


class StatsService(CommonService):
    def __init__(self, db: Session):
        super().__init__(db)

    def list_stats(self) -> List[StatsResponse]:
        stats_list = self.db.query(Stats).all()
        return [self._to_response(stats) for stats in stats_list]

    def create_stats(
        self,
        payload: StatsCreate,
    ) -> StatsResponse:
        stats = Stats()
        self.db.add(stats)
        self.db.flush()

        self._replace_metrics(stats.id, payload.metrics)

        self.db.commit()
        self.db.refresh(stats)
        return self._to_response(stats)

    def get_stats(
        self,
        stats_id: int,
    ) -> StatsResponse:
        stats = self._get_stats_or_404(stats_id)
        return self._to_response(stats)

    def update_stats(
        self,
        stats_id: int,
        payload: StatsUpdate,
    ) -> StatsResponse:
        stats = self._get_stats_or_404(stats_id)
        data = payload.model_dump(exclude_unset=True)

        if "metrics" in data:
            self._replace_metrics(stats_id, data["metrics"])

        self.db.commit()
        self.db.refresh(stats)
        return self._to_response(stats)

    def delete_stats(
        self,
        stats_id: int,
    ) -> None:
        stats = self._get_stats_or_404(stats_id)
        (
            self.db.query(CrossMetricStats)
            .filter(CrossMetricStats.stats_id == stats_id)
            .delete(synchronize_session=False)
        )
        self.db.delete(stats)
        self.db.commit()

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
            metric = Metric(name=metric_item.name, value=metric_item.value)
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
