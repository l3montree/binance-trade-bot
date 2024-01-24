from sqlalchemy import Column, Float, ForeignKey, Integer, String, func, or_, select
from sqlalchemy.orm import column_property, relationship

from .base import Base
from .coin import Coin


class Pair(Base):
    __tablename__ = "pairs"

    id = Column(Integer, primary_key=True) #creates a column which has the primary keys --> unique identifier for each row?

    #code below: sets relationships between 2 x (coin and pair) and links each to different ids: to_coin, from_coin
    from_coin_id = Column(String, ForeignKey("coins.symbol")) #creates a column of strings where values in each row relate to values in the "coins.symbol" column
    from_coin = relationship("Coin", foreign_keys=[from_coin_id], lazy="joined") #sets a link between coin and pair

    to_coin_id = Column(String, ForeignKey("coins.symbol"))
    to_coin = relationship("Coin", foreign_keys=[to_coin_id], lazy="joined")

    ratio = Column(Float) #creates a new column linked to ratio

    enabled = column_property(
        select([func.count(Coin.symbol)==2])
        .where(or_(Coin.symbol == from_coin_id, Coin.symbol == to_coin_id))
        .where(Coin.enabled.is_(True))
        .as_scalar()
    )

    def __init__(self, from_coin: Coin, to_coin: Coin, ratio=None):
        self.from_coin = from_coin
        self.to_coin = to_coin
        self.ratio = ratio

    def __repr__(self):
        return f"<{self.from_coin_id}->{self.to_coin_id} :: {self.ratio}>"

    def info(self):
        return {
            "from_coin": self.from_coin.info(),
            "to_coin": self.to_coin.info(),
            "ratio": self.ratio,
        }
