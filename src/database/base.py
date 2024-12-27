from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id:       Mapped[int] = mapped_column(primary_key=True)
class Test(Base):
    title:    Mapped[str] = mapped_column(nullable=False)
class User(Base):
    uid:      Mapped[int] = mapped_column(nullable=False) # telegram user id
    coins:    Mapped[int] = mapped_column(nullable=False, default=0)
    # diamonds: Mapped[int] = mapped_column(nullable=False, default=0)
    # energy:   Mapped[int] = mapped_column(nullable=False, default=1000)
    # full:     Mapped[int] = mapped_column(nullable=False, default=3) # full energy amount
    # turbo:    Mapped[int] = mapped_column(nullable=False, default=3) # turbo amount
    friend:   Mapped[int] = mapped_column(nullable=False, default=0) # friend id
    avatar:   Mapped[int] = mapped_column(nullable=False, default=1)
    login:    Mapped[int] = mapped_column(nullable=False) # last login timestamp
    status:   Mapped[str] = mapped_column(nullable=False, default="active") # active | ban
class Avatar(Base):
    title:    Mapped[str] = mapped_column(nullable=False)
class Task(Base):
    title:    Mapped[str] = mapped_column(nullable=False)
    # image:    Mapped[str] = mapped_column(nullable=False)
    coins:    Mapped[int] = mapped_column(nullable=False)
    diamonds: Mapped[int] = mapped_column(nullable=False)
# class TaskDone(Base):
#     tid:      Mapped[int] = mapped_column(nullable=False) # task id
#     uid:      Mapped[int] = mapped_column(nullable=False) # user id which complete this task
