from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    password = Column(String(128), nullable=False)
    email = Column(String(255))
    first_name = Column(String(120))
    last_name = Column(String(120))
    organization = Column(String(180))


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
    source = Column(String(4), default="IPTC")


class Descriptor(Base):
    __tablename__ = "descriptor"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), nullable=False)


class AlertCategoryItem(Base):
    __tablename__ = "alert_category_item"

    code = Column(String(60), primary_key=True)
    label = Column(String(120), nullable=False)


class Metric(Base):
    __tablename__ = "metric"

    name = Column(String(100), primary_key=True)
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


class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    alert_id = Column(Integer, ForeignKey("alert.id", ondelete="CASCADE"))
    timestamp = Column(DateTime, nullable=False)


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
