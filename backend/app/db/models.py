from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
import re

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    password = Column(String(128), nullable=False)
    email = Column(String(255))
    first_name = Column(String(120))
    last_name = Column(String(120))
    organization = Column(String(180))
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(String(255), nullable=True, unique=True)
    verification_token_expires_at = Column(DateTime, nullable=True)
    reset_password_token = Column(String(100), unique=True, nullable=True)
    reset_password_expires_at = Column(DateTime, nullable=True)


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)


class InformationSource(Base):
    __tablename__ = "information_source"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(120), nullable=False)
    url = Column(String(2048), nullable=False)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(120), nullable=False)
    source = Column(String(8), default="IPTC")
    code = Column(String(8), nullable=True)


class Descriptor(Base):
    __tablename__ = "descriptor"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), nullable=False)


class AlertCategoryItem(Base):
    __tablename__ = "alert_category_item"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    code = Column(String(60), nullable=False)
    label = Column(String(120), nullable=False)


class Metric(Base):
    __tablename__ = "metric"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)


class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, autoincrement="auto")


class ActiveToken(Base):
    __tablename__ = "active_token"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))


class Alert(Base):
    __tablename__ = "alert"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String(200), nullable=False)
    cron_expression = Column(String(120), nullable=False)


# ---------------------------------------------------------------------------
# NewsItem — registro de cada noticia procesada por el motor de monitorización.
#
# Por qué existe esta tabla:
#   El mismo artículo puede aparecer en un feed RSS durante días. Sin esta
#   tabla, cada ejecución del cron volvería a detectarlo y generaría
#   notificaciones duplicadas. La URL del artículo es el identificador
#   natural y único de una noticia en la web.
#
# Campos:
#   url         — URL canónica del artículo. Clave de deduplicación.
#   title       — Título extraído del campo <title> del item RSS.
#   summary     — Resumen extraído del campo <summary> o <description>.
#   published   — Fecha de publicación según el feed (puede ser None si
#                 el feed no la incluye).
#   channel_id  — Canal RSS del que proviene, para trazabilidad.
#   created_at  — Momento en que nuestro sistema lo procesó por primera vez.
# ---------------------------------------------------------------------------
class NewsItem(Base):
    __tablename__ = "news_item"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    url = Column(String(2048), nullable=False, unique=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    published = Column(DateTime, nullable=True)
    channel_id = Column(Integer, ForeignKey("rss_channel.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, nullable=False)


# ---------------------------------------------------------------------------
# Notification — notificación generada cuando una noticia coincide con una
# alerta activa.
#
# Cambios respecto al modelo original:
#   Se añaden news_item_id, matched_descriptor y is_read.
#
#   news_item_id      — Referencia a la noticia que disparó la notificación.
#                       Permite al frontend mostrar el título, URL y resumen
#                       sin duplicar datos.
#   matched_descriptor — El descriptor concreto (palabra clave) que causó
#                        el match. Útil para el asunto del email:
#                        "Actualización de <alerta> en <día/hora>".
#   is_read           — Indica si el usuario ya leyó la notificación en
#                       el buzón de la aplicación. Necesario para el panel
#                       (Sprint 3).
#
# La restricción UniqueConstraint (alert_id, news_item_id) garantiza que
# una misma noticia no genere dos notificaciones para la misma alerta,
# incluso si dos descriptores de esa alerta hacen match con el mismo artículo.
# ---------------------------------------------------------------------------
class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    alert_id = Column(Integer, ForeignKey("alert.id", ondelete="CASCADE"))
    news_item_id = Column(Integer, ForeignKey("news_item.id", ondelete="CASCADE"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    matched_descriptor = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("alert_id", "news_item_id", name="uq_notification_alert_news"),
    )


class RSSChannel(Base):
    __tablename__ = "rss_channel"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    information_source_id = Column(
        Integer, ForeignKey("information_source.id", ondelete="CASCADE")
    )
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
    url = Column(String(2048), nullable=False)


class CrossRoleUser(Base):
    __tablename__ = "cross_role_user"

    role_id = Column(
        Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )


class CrossAlertDescriptor(Base):
    __tablename__ = "cross_alert_descriptor"

    alert_id = Column(
        Integer, ForeignKey("alert.id", ondelete="CASCADE"), primary_key=True
    )
    descriptor_id = Column(
        Integer, ForeignKey("descriptor.id", ondelete="CASCADE"), primary_key=True
    )


class CrossMetricNotification(Base):
    __tablename__ = "cross_metric_notification"

    metric_id = Column(
        Integer, ForeignKey("metric.id", ondelete="CASCADE"), primary_key=True
    )
    notification_id = Column(
        Integer, ForeignKey("notification.id", ondelete="CASCADE"), primary_key=True
    )


class CrossAlertAlertCategoryItem(Base):
    __tablename__ = "cross_alert_alert_category_item"

    alert_id = Column(
        Integer, ForeignKey("alert.id", ondelete="CASCADE"), primary_key=True
    )
    alert_category_item_id = Column(
        Integer,
        ForeignKey("alert_category_item.id", ondelete="CASCADE"),
        primary_key=True,
    )


class CrossMetricStats(Base):
    __tablename__ = "cross_metric_stats"

    metric_id = Column(
        Integer, ForeignKey("metric.id", ondelete="CASCADE"), primary_key=True
    )
    stats_id = Column(
        Integer, ForeignKey("stats.id", ondelete="CASCADE"), primary_key=True
    )