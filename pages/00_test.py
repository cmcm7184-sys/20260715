# app.py
# Trade Simulator v1.0

from market import Market
from trade import TradeSystem
from event import EventSystem


def main():
    print("=" * 50)
    print("🌎 GLOBAL TRADE SIMULATOR v1.0")
    print("=" * 50)

    market = Market()
    trade = TradeSystem(market)
    event = EventSystem(market)

    country = input("국가 선택: ")

    if country not in market.countries:
        print("없는 국가입니다.")
        return

    money = 1000000

    while True:
        print("\n---------------------------")
        print(f"국가 : {country}")
        print(f"자금 : ${money:,}")
        print("---------------------------")
        print("1. 시장 보기")
        print("2. 제품 구매")
        print("3. 제품 판매")
        print("4. 국가 이벤트")
        print("5. 종료")

        cmd = input("> ")

        if cmd == "1":
            market.show_products()

        elif cmd == "2":
            money = trade.buy(country, money)

        elif cmd == "3":
            money = trade.sell(country, money)

        elif cmd == "4":
            event.random_event()

        elif cmd == "5":
            print("게임 종료")
            break

        else:
            print("잘못 입력")


if __name__ == "__main__":
    main()
  # market.py
# 국가별 무역 시장 데이터

class Market:

    def __init__(self):

        self.countries = {
            "중국": {
                "GDP": 18000,
                "export": 3500
            },
            "미국": {
                "GDP": 28000,
                "export": 2000
            },
            "한국": {
                "GDP": 1800,
                "export": 700
            },
            "일본": {
                "GDP": 4200,
                "export": 900
            },
            "독일": {
                "GDP": 4500,
                "export": 1700
            },
            "네덜란드": {
                "GDP": 1100,
                "export": 900
            }
        }


        self.products = {

            "반도체": {
                "price": 10000,
                "demand": 90
            },

            "자동차": {
                "price": 30000,
                "demand": 70
            },

            "석유": {
                "price": 5000,
                "demand": 80
            },

            "농산물": {
                "price": 3000,
                "demand": 60
            },

            "배터리": {
                "price": 15000,
                "demand": 85
            }
        }


    def show_products(self):

        print("\n===== 현재 시장 =====")

        for name, data in self.products.items():

            print(
                f"{name} | 가격: {data['price']:,}원 | 수요: {data['demand']}%"
            )


    def change_price(self, product, value):

        if product in self.products:

            self.products[product]["price"] += value

            if self.products[product]["price"] < 100:
                self.products[product]["price"] = 100


    def get_price(self, product):
# trade.py
# 무역 거래 시스템

class TradeSystem:

    def __init__(self, market):

        self.market = market

        self.inventory = {}


    def buy(self, country, money):

        print("\n구매 가능한 상품")

        self.market.show_products()

        product = input("\n구매할 상품: ")

        if product not in self.market.products:

            print("없는 상품입니다.")
            return money


        price = self.market.get_price(product)

        amount = int(input("구매 수량: "))

        cost = price * amount


        if money < cost:

            print("자금 부족")
            return money


        money -= cost


        if product not in self.inventory:

            self.inventory[product] = 0


        self.inventory[product] += amount


        print(
            f"{product} {amount}개 구매 완료"
        )

        return money



    def sell(self, country, money):

        if len(self.inventory) == 0:

            print("판매할 상품 없음")
            return money


        print("\n보유 상품")

        for item, amount in self.inventory.items():

            print(item, amount)


        product = input("판매할 상품: ")


        if product not in self.inventory:

            print("보유하지 않은 상품")
            return money


        amount = int(input("판매 수량: "))


        if amount > self.inventory[product]:

            print("수량 부족")
            return money


        price = self.market.get_price(product)


        income = price * amount


        money += income


        self.inventory[product] -= amount


        print(
            f"{product} {amount}개 판매 +{income:,}원"
        )


        return money
      # event.py
# 세계 경제 이벤트 시스템

import random


class EventSystem:

    def __init__(self, market):

        self.market = market


        self.events = [

            {
                "name": "세계 반도체 부족 발생",
                "effect": {
                    "반도체": 5000
                }
            },


            {
                "name": "국제 유가 상승",
                "effect": {
                    "석유": 3000
                }
            },


            {
                "name": "세계 경기 침체",
                "effect": {
                    "자동차": -5000,
                    "농산물": 1000
                }
            },


            {
                "name": "친환경 산업 성장",
                "effect": {
                    "배터리": 4000
                }
            },


            {
                "name": "무역 갈등 발생",
                "effect": {
                    "반도체": -3000,
                    "자동차": -2000
                }
            }

        ]



    def random_event(self):

        event = random.choice(self.events)


        print("\n🌍 세계 이벤트 발생!")
        print(event["name"])


        for product, change in event["effect"].items():

            self.market.change_price(
                product,
                change
            )

            if change > 0:
                print(
                    f"{product} 가격 상승 +{change:,}원"
                )

            else:
                print(
                    f"{product} 가격 하락 {change:,}원"
                )
              # data.py
# 국가별 무역 데이터 (단위: 10억 달러)

trade_data = {

    "중국": {
        2017: 2216.2,
        2018: 2417.4,
        2019: 2386.6,
        2020: 2510.0,
        2021: 3215.8,
        2022: 3340.0,
        2023: 3220.0,
        2024: 3400.0
    },


    "미국": {
        2017: 1546.0,
        2018: 1664.0,
        2019: 1645.0,
        2020: 1424.0,
        2021: 1754.0,
        2022: 2080.0,
        2023: 2030.0,
        2024: 2100.0
    },


    "한국": {
        2017: 573.7,
        2018: 605.2,
        2019: 542.2,
        2020: 512.5,
        2021: 644.4,
        2022: 683.6,
        2023: 632.7,
        2024: 683.8
    },


    "일본": {
        2017: 698.0,
        2018: 738.0,
        2019: 705.0,
        2020: 640.0,
        2021: 756.0,
        2022: 756.0,
        2023: 717.0,
        2024: 730.0
    },


    "독일": {
        2017: 1448.0,
        2018: 1560.0,
        2019: 1489.0,
        2020: 1379.0,
        2021: 1640.0,
        2022: 1680.0,
        2023: 1690.0,
        2024: 1720.0
    },


    "네덜란드": {
        2017: 651.0,
        2018: 723.0,
        2019: 709.0,
        2020: 674.0,
        2021: 837.0,
        2022: 965.0,
        2023: 934.0,
        2024: 960.0
    }

}



def get_trade(country, year):

    if country in trade_data:

        if year in trade_data[country]:

            return trade_data[country][year]


    return 0



def show_trade(country):

    if country not in trade_data:

        print("없는 국가")
        return


    print("\n===== 무역 규모 =====")


    for year, value in trade_data[country].items():

        print(
            f"{year}년 : {value} (10억 달러)"
        )
      # main.py
# Global Trade Simulator 연결 파일

from market import Market
from trade import TradeSystem
from event import EventSystem
from data import show_trade


def main():

    print("=" * 50)
    print("🌎 GLOBAL TRADE SIMULATOR v1.1")
    print("=" * 50)


    market = Market()
    trade = TradeSystem(market)
    event = EventSystem(market)


    countries = [
        "중국",
        "미국",
        "한국",
        "일본",
        "독일",
        "네덜란드"
    ]


    print("\n선택 가능한 국가")

    for c in countries:
        print("-", c)



    country = input("\n플레이 국가 선택 : ")


    if country not in countries:

        print("국가 선택 오류")
        return



    money = 1000000



    while True:

        print("\n" + "="*40)

        print(f"현재 국가 : {country}")
        print(f"보유 자금 : {money:,}원")

        print("="*40)


        print("""
1. 시장 확인
2. 상품 구매
3. 상품 판매
4. 국가 무역 규모 확인
5. 세계 이벤트 발생
6. 종료
""")


        command = input("> ")



        if command == "1":

            market.show_products()



        elif command == "2":

            money = trade.buy(
                country,
                money
            )



        elif command == "3":

            money = trade.sell(
                country,
                money
            )



        elif command == "4":

            show_trade(country)



        elif command == "5":

            event.random_event()



        elif command == "6":

            print("게임 종료")
            break



        else:

            print("잘못된 입력")




if __name__ == "__main__":

    main()
  # upgrade.py
# 국가 능력치 / 경제 시스템 확장

class CountrySystem:


    def __init__(self):

        self.countries = {

            "중국": {
                "GDP": 18000,
                "currency": 7.2,
                "tax": 0.10,
                "power": 95
            },


            "미국": {
                "GDP": 28000,
                "currency": 1,
                "tax": 0.08,
                "power": 100
            },


            "한국": {
                "GDP": 1800,
                "currency": 1300,
                "tax": 0.12,
                "power": 75
            },


            "일본": {
                "GDP": 4200,
                "currency": 150,
                "tax": 0.11,
                "power": 80
            },


            "독일": {
                "GDP": 4500,
                "currency": 1,
                "tax": 0.09,
                "power": 85
            },


            "네덜란드": {
                "GDP": 1100,
                "currency": 1,
                "tax": 0.09,
                "power": 78
            }

        }



    def show_country(self, country):

        if country not in self.countries:

            print("국가 없음")
            return


        data = self.countries[country]


        print("\n===== 국가 정보 =====")

        print(
            f"국가 : {country}"
        )

        print(
            f"GDP : {data['GDP']}B 달러"
        )

        print(
            f"환율 : {data['currency']}"
        )

        print(
            f"관세율 : {data['tax']*100}%"
        )

        print(
            f"경제력 : {data['power']}/100"
        )



    def apply_tariff(self, country, price):

        if country in self.countries:

            tariff = self.countries[country]["tax"]

            return price * (1 + tariff)


        return price
      # diplomacy.py
# 국가 관계 / 무역 협정 / 제재 시스템


class DiplomacySystem:


    def __init__(self):

        self.relations = {


            ("미국", "중국"): -30,
            ("미국", "한국"): 70,
            ("미국", "일본"): 85,
            ("미국", "독일"): 75,
            ("미국", "네덜란드"): 80,


            ("중국", "한국"): 50,
            ("중국", "일본"): 20,
            ("중국", "독일"): 60,
            ("중국", "네덜란드"): 55,


            ("한국", "일본"): 40,
            ("한국", "독일"): 65,
            ("한국", "네덜란드"): 70,


            ("일본", "독일"): 70,
            ("일본", "네덜란드"): 65,


            ("독일", "네덜란드"): 90

        }



        self.agreements = []




    def get_relation(self, country1, country2):

        key = (country1, country2)

        reverse = (country2, country1)


        if key in self.relations:

            return self.relations[key]


        elif reverse in self.relations:

            return self.relations[reverse]


        return 0




    def show_relation(self, country1, country2):

        value = self.get_relation(
            country1,
            country2
        )


        print(
            f"{country1} - {country2} 관계도 : {value}"
        )


        if value >= 70:

            print("우호 관계 🤝")


        elif value >= 30:

            print("보통 관계")


        else:

            print("긴장 관계 ⚠️")




    def trade_agreement(self, country1, country2):

        value = self.get_relation(
            country1,
            country2
        )


        if value >= 50:

            self.agreements.append(
                (country1, country2)
            )

            print(
                "무역 협정 체결 성공!"
            )

            print(
                f"{country1} ↔ {country2}"
            )


        else:

            print(
                "관계가 나빠 협정 실패"
            )




    def apply_sanction(self, country1, country2):

        print(
            f"{country1}가 {country2}에 경제 제재 실시"
        )


        key = (country1, country2)


        if key in self.relations:

            self.relations[key] -= 20

        else:

            self.relations[(country1, country2)] = -20


        print(
            "양국 관계 악화"
        )
      # war_event.py
# 전쟁 / 국제 위기 이벤트 시스템


import random



class WarEventSystem:


    def __init__(self, market):

        self.market = market



        self.events = [

            {
                "name": "중동 지역 전쟁 발생",
                "effects": {
                    "석유": 8000,
                    "자동차": -3000
                }
            },


            {
                "name": "미중 무역 갈등 심화",
                "effects": {
                    "반도체": -5000,
                    "배터리": -3000
                }
            },


            {
                "name": "세계 금융 위기",
                "effects": {
                    "자동차": -7000,
                    "농산물": 3000
                }
            },


            {
                "name": "국제 평화 협정 체결",
                "effects": {
                    "반도체": 4000,
                    "자동차": 4000
                }
            },


            {
                "name": "공급망 붕괴",
                "effects": {
                    "반도체": 7000,
                    "배터리": 5000
                }
            }

        ]




    def start_event(self):


        event = random.choice(
            self.events
        )


        print("\n🚨 국제 사건 발생")
        print(
            event["name"]
        )


        for product, change in event["effects"].items():


            self.market.change_price(
                product,
                change
            )


            if change > 0:

                print(
                    f"{product} 가격 상승 +{change:,}원"
                )


            else:

                print(
                    f"{product} 가격 하락 {change:,}원"
                )
              # finance.py
# 금융 시스템 (은행 / 대출 / 투자 / 파산)


class FinanceSystem:


    def __init__(self):

        self.loan = 0

        self.investment = 0




    def borrow(self, money):

        amount = int(
            input("대출 금액 입력: ")
        )


        self.loan += amount

        money += amount


        print(
            f"{amount:,}원 대출 완료"
        )

        print(
            f"현재 부채: {self.loan:,}원"
        )


        return money





    def repay(self, money):

        if self.loan == 0:

            print("갚을 대출 없음")
            return money



        amount = int(
            input("상환 금액 입력: ")
        )


        if amount > money:

            print("자금 부족")
            return money



        if amount > self.loan:

            amount = self.loan



        money -= amount

        self.loan -= amount



        print(
            f"{amount:,}원 상환 완료"
        )

        return money





    def invest(self, money):

        amount = int(
            input("투자 금액 입력: ")
        )


        if amount > money:

            print("투자 불가능")
            return money



        self.investment += amount

        money -= amount



        print(
            f"{amount:,}원 투자 완료"
        )


        return money





    def market_result(self, money):

        if self.investment == 0:

            return money



        import random


        rate = random.randint(
            -20,
            30
        )


        result = int(
            self.investment *
            (1 + rate/100)
        )


        money += result


        print(
            f"투자 결과 : {rate}%"
        )

        print(
            f"{result:,}원 회수"
        )


        self.investment = 0


        return money





    def check_status(self):

        print("\n===== 금융 상태 =====")

        print(
            f"대출 : {self.loan:,}원"
        )

        print(
            f"투자금 : {self.investment:,}원"
        )
      # company.py
# 기업 설립 / 생산 / 고용 / 수출 시스템


class CompanySystem:


    def __init__(self):

        self.company = None

        self.money = 0

        self.workers = 0

        self.production = {}




    def create_company(self):

        name = input("기업 이름 입력: ")

        self.company = name

        self.money = 500000


        print(
            f"{name} 설립 완료!"
        )

        print(
            "초기 자본: 500,000원"
        )





    def hire(self):

        if self.company is None:

            print("기업이 없습니다")
            return



        count = int(
            input("고용할 직원 수: ")
        )


        cost = count * 10000


        if cost > self.money:

            print("자금 부족")
            return



        self.money -= cost

        self.workers += count



        print(
            f"{count}명 고용 완료"
        )





    def produce(self):

        if self.workers == 0:

            print("직원이 없습니다")
            return



        print("""
생산 제품

1. 반도체
2. 자동차
3. 배터리
4. 농산물
""")


        choice = input("제품 선택: ")



        products = {

            "1": "반도체",
            "2": "자동차",
            "3": "배터리",
            "4": "농산물"

        }



        if choice not in products:

            print("잘못 입력")
            return



        product = products[choice]


        amount = self.workers * 10


        if product not in self.production:

            self.production[product] = 0



        self.production[product] += amount



        print(
            f"{product} {amount}개 생산"
        )





    def export(self, market):


        if len(self.production) == 0:

            print("수출할 제품 없음")
            return



        print("\n보유 제품")


        for p, a in self.production.items():

            print(
                p,
                a
            )



        product = input(
            "수출 제품: "
        )


        if product not in self.production:

            print("제품 없음")
            return



        amount = self.production[product]


        price = market.get_price(product)



        income = amount * price



        self.money += income



        self.production[product] = 0



        print(
            f"{product} 수출 성공"
        )

        print(
            f"수익 +{income:,}원"
        )





    def status(self):

        print("\n===== 기업 현황 =====")

        print(
            "기업:",
            self.company
        )

        print(
            "자금:",
            f"{self.money:,}원"
        )

        print(
            "직원:",
            self.workers,
            "명"
        )

        print(
            "생산:",
            self.production
        )
      # save.py
# 게임 저장 / 불러오기 시스템

import json



class SaveSystem:


    def __init__(self):

        self.file = "save_data.json"




    def save(self, data):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:


                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )


            print("💾 저장 완료")


        except:

            print("저장 실패")





    def load(self):

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:


                data = json.load(f)



            print("📂 불러오기 완료")


            return data



        except:


            print("저장 데이터 없음")


            return None
          # achievement.py
# 업적 / 승리 조건 / 랭킹 시스템


class AchievementSystem:


    def __init__(self):

        self.achievements = {

            "첫 무역 성공": False,
            "100만 달러 기업": False,
            "세계 수출 1위": False,
            "경제 대국 달성": False,
            "무역 제국 건설": False

        }





    def check(self, money, export, country_rank):


        if export >= 1:

            self.achievements["첫 무역 성공"] = True



        if money >= 1000000:

            self.achievements["100만 달러 기업"] = True



        if country_rank == 1:

            self.achievements["세계 수출 1위"] = True



        if money >= 10000000:

            self.achievements["경제 대국 달성"] = True



        if money >= 50000000 and export >= 100:

            self.achievements["무역 제국 건설"] = True





    def show(self):


        print("\n===== 🏆 업적 =====")


        for name, value in self.achievements.items():


            if value:

                print("✅", name)


            else:

                print("⬜", name)





    def ranking(self, countries):


        print("\n===== 🌎 국가 경제 순위 =====")


        sorted_country = sorted(
            countries.items(),
            key=lambda x: x[1],
            reverse=True
        )


        rank = 1


        for country, value in sorted_country:


            print(
                f"{rank}위 {country} : {value:,}"
            )


            rank += 1
          # technology.py
# 기술 개발 / 연구 투자 / 산업 성장 시스템


class TechnologySystem:


    def __init__(self):

        self.tech_level = {

            "반도체": 1,
            "자동차": 1,
            "배터리": 1,
            "AI": 1,
            "친환경": 1

        }



        self.research_point = 0




    def invest_research(self, money):


        cost = int(
            input("연구 투자 금액: ")
        )


        if cost > money:

            print("자금 부족")
            return money



        money -= cost


        self.research_point += cost // 10000


        print(
            f"연구 포인트 +{cost//10000}"
        )


        return money





    def develop(self):


        print("\n개발 가능한 기술")

        for tech in self.tech_level:

            print(
                tech,
                "Lv.",
                self.tech_level[tech]
            )



        target = input(
            "개발할 기술: "
        )



        if target not in self.tech_level:

            print("없는 기술")
            return



        needed = self.tech_level[target] * 10



        if self.research_point < needed:

            print("연구 포인트 부족")
            return



        self.research_point -= needed


        self.tech_level[target] += 1



        print(
            f"{target} 기술 발전!"
        )

        print(
            f"현재 Lv.{self.tech_level[target]}"
        )





    def apply_bonus(self, product):


        if product in self.tech_level:


            level = self.tech_level[product]


            return level * 5



        return 0





    def show(self):


        print("\n===== 🔬 기술 현황 =====")


        for tech, level in self.tech_level.items():


            print(
                f"{tech} : Lv.{level}"
            )


        print(
            "연구 포인트:",
            self.research_point
        )
      # world_market.py
# 세계 시장 가격 / 수요 / 공급 AI 시스템


import random



class WorldMarketSystem:


    def __init__(self):


        self.market = {


            "반도체": {
                "price": 10000,
                "supply": 70,
                "demand": 90
            },


            "자동차": {
                "price": 30000,
                "supply": 80,
                "demand": 70
            },


            "석유": {
                "price": 5000,
                "supply": 90,
                "demand": 85
            },


            "배터리": {
                "price": 15000,
                "supply": 60,
                "demand": 95
            },


            "농산물": {
                "price": 3000,
                "supply": 85,
                "demand": 60
            }

        }




    def update_market(self):


        print("\n🌐 세계 시장 변화")


        for product, data in self.market.items():


            change = random.randint(
                -10,
                10
            )


            data["demand"] += change


            if data["demand"] < 10:

                data["demand"] = 10


            if data["demand"] > 100:

                data["demand"] = 100



            # 수요와 공급에 따른 가격 변화

            if data["demand"] > data["supply"]:

                data["price"] += 1000

            else:

                data["price"] -= 500



            if data["price"] < 100:

                data["price"] = 100





    def show(self):


        print("\n===== 🌎 세계 시장 =====")


        for product, data in self.market.items():


            print(
                f"{product} | "
                f"가격:{data['price']:,}원 | "
                f"수요:{data['demand']} | "
                f"공급:{data['supply']}"
            )





    def get_price(self, product):


        if product in self.market:

            return self.market[product]["price"]


        return 0





    def trade_effect(self, product, amount):


        if product not in self.market:

            return



        self.market[product]["supply"] += amount // 10



        if self.market[product]["supply"] > 100:

            self.market[product]["supply"] = 100
          # ai_country.py
# 컴퓨터 국가 AI 시스템
# 생산 / 무역 / 성장 / 경쟁


import random



class AICountrySystem:


    def __init__(self):


        self.countries = {


            "미국": {

                "money": 5000000,
                "industry": 90,
                "export": 100

            },


            "중국": {

                "money": 4500000,
                "industry": 95,
                "export": 120

            },


            "독일": {

                "money": 3000000,
                "industry": 85,
                "export": 90

            },


            "일본": {

                "money": 2800000,
                "industry": 80,
                "export": 80

            },


            "한국": {

                "money": 2000000,
                "industry": 85,
                "export": 70

            },


            "네덜란드": {

                "money": 1500000,
                "industry": 75,
                "export": 85

            }


        }





    def ai_turn(self):


        print("\n🤖 AI 국가 행동")


        for country, data in self.countries.items():


            action = random.choice(

                [
                    "produce",
                    "trade",
                    "research"
                ]

            )



            if action == "produce":


                profit = data["industry"] * 10000


                data["money"] += profit


                data["export"] += 1



                print(
                    f"{country}: 생산 확대 +{profit:,}원"
                )




            elif action == "trade":


                profit = random.randint(
                    10000,
                    100000
                )


                data["money"] += profit


                data["export"] += 2



                print(
                    f"{country}: 무역 성공 +{profit:,}원"
                )





            else:


                data["industry"] += 1


                print(
                    f"{country}: 기술 투자 산업력 증가"
                )







    def ranking(self):


        print("\n===== 🌎 세계 경제 순위 =====")


        ranking = sorted(

            self.countries.items(),

            key=lambda x:x[1]["money"],

            reverse=True

        )


        rank = 1



        for country, data in ranking:


            print(

                f"{rank}위 {country} "
                f"| 자본:{data['money']:,}원 "
                f"| 수출:{data['export']}"

            )


            rank += 1
          # random_event_plus.py
# 대형 세계 경제 이벤트 시스템
# 코로나 / 금융위기 / 전쟁 / 원자재 쇼크


import random



class GlobalEventSystem:


    def __init__(self, market):


        self.market = market



        self.events = [


            {

                "name": "🦠 세계적 감염병 확산",

                "effects": {

                    "자동차": -7000,
                    "석유": -3000,
                    "농산물": 3000,
                    "배터리": 2000

                }

            },


            {

                "name": "💰 글로벌 금융 위기",

                "effects": {

                    "자동차": -10000,
                    "반도체": -5000,
                    "석유": -4000

                }

            },


            {

                "name": "⚔️ 국제 전쟁 발생",

                "effects": {

                    "석유": 12000,
                    "농산물": 5000,
                    "자동차": -4000

                }

            },


            {

                "name": "🚢 세계 공급망 붕괴",

                "effects": {

                    "반도체": 15000,
                    "배터리": 8000,
                    "자동차": -5000

                }

            },


            {

                "name": "🤝 자유무역 확대",

                "effects": {

                    "반도체": 5000,
                    "자동차": 5000,
                    "배터리": 5000

                }

            },


            {

                "name": "🛢️ 원유 생산 감소",

                "effects": {

                    "석유": 15000

                }

            },


            {

                "name": "🌱 친환경 정책 강화",

                "effects": {

                    "배터리": 12000,
                    "석유": -5000

                }

            }

        ]






    def trigger(self):


        event = random.choice(
            self.events
        )


        print("\n====================")

        print(
            "🌍 세계 사건 발생"
        )

        print(
            event["name"]
        )

        print(
            "===================="
        )



        for product, change in event["effects"].items():


            self.market.change_price(
                product,
                change
            )


            if change > 0:

                print(
                    f"{product} 가격 상승 +{change:,}원"
                )


            else:

                print(
                    f"{product} 가격 하락 {change:,}원"
                )





    def custom_event(self):


        print("""
직접 이벤트 설정

1. 전쟁
2. 무역협정
3. 경제위기
""")


        choice = input("> ")



        if choice == "1":

            print(
                "전쟁 발생: 석유 가격 상승"
            )

            self.market.change_price(
                "석유",
                10000
            )



        elif choice == "2":

            print(
                "무역 확대: 전체 산업 성장"
            )


            for product in self.market.products:

                self.market.change_price(
                    product,
                    2000
                )



        elif choice == "3":

            print(
                "경제위기 발생"
            )


            for product in self.market.products:

                self.market.change_price(
                    product,
                    -3000
                )



        else:

            print(
                "잘못된 선택"
            )
          # government.py
# 정부 정책 시스템
# 세금 / 보조금 / 금리 / 통화 정책


class GovernmentSystem:


    def __init__(self):


        self.policy = {


            "tax": 10,          # 세율 %

            "interest": 3,      # 기준금리 %

            "subsidy": 0,       # 산업 보조금

            "currency": 100     # 화폐 가치


        }





    def show_policy(self):


        print("\n===== 🏛 정부 정책 =====")


        print(
            f"세율 : {self.policy['tax']}%"
        )


        print(
            f"금리 : {self.policy['interest']}%"
        )


        print(
            f"산업 보조금 : {self.policy['subsidy']:,}원"
        )


        print(
            f"화폐 가치 : {self.policy['currency']}"
        )





    def reduce_tax(self):


        if self.policy["tax"] > 1:


            self.policy["tax"] -= 1


            print(
                "감세 정책 시행"
            )


            print(
                "기업 투자 증가"
            )



    def increase_tax(self):


        self.policy["tax"] += 1


        print(
            "증세 정책 시행"
        )


        print(
            "정부 재정 증가"
        )





    def lower_interest(self):


        if self.policy["interest"] > 0:


            self.policy["interest"] -= 1


            print(
                "금리 인하"
            )


            print(
                "소비와 투자 증가"
            )





    def raise_interest(self):


        self.policy["interest"] += 1


        print(
            "금리 인상"
        )


        print(
            "물가 안정 효과"
        )





    def give_subsidy(self, industry):


        industries = {


            "반도체": 50000,

            "배터리": 40000,

            "자동차": 30000,

            "친환경": 35000


        }



        if industry in industries:


            amount = industries[industry]


            self.policy["subsidy"] += amount


            print(
                f"{industry} 산업 보조금 지급"
            )


            print(
                f"+{amount:,}원"
            )


        else:

            print(
                "지원 불가능 산업"
            )





    def apply_policy(self, market):


        tax_effect = self.policy["tax"] * 100


        for product in market.products:


            market.change_price(
                product,
                -tax_effect
            )


        print(
            "정부 정책이 시장에 적용됨"
        )
      # statistics.py
# 경제 데이터 분석 시스템
# GDP / 무역량 / 성장률 계산


class StatisticsSystem:


    def __init__(self):


        self.history = {}





    def add_data(self, country, year, value):


        if country not in self.history:

            self.history[country] = {}



        self.history[country][year] = value





    def show_history(self, country):


        if country not in self.history:


            print("데이터 없음")

            return



        print(
            f"\n===== {country} 경제 변화 ====="
        )



        for year, value in self.history[country].items():


            print(
                f"{year}년 : {value:,}"
            )





    def growth_rate(self, country, start, end):


        if country not in self.history:

            return 0



        old = self.history[country].get(start)

        new = self.history[country].get(end)



        if old is None or new is None:

            return 0



        rate = ((new-old)/old)*100



        return round(rate,2)





    def compare(self, country1, country2, year):


        value1 = self.history.get(
            country1,
            {}
        ).get(year,0)



        value2 = self.history.get(
            country2,
            {}
        ).get(year,0)



        print(
            "\n===== 국가 비교 ====="
        )


        print(
            f"{country1}: {value1:,}"
        )


        print(
            f"{country2}: {value2:,}"
        )



        if value1 > value2:


            print(
                f"{country1} 우위"
            )


        elif value2 > value1:


            print(
                f"{country2} 우위"
            )


        else:


            print(
                "동일"
            )





    def ranking(self, year):


        result = []



        for country, data in self.history.items():


            if year in data:


                result.append(
                    (
                        country,
                        data[year]
                    )
                )



        result.sort(
            key=lambda x:x[1],
            reverse=True
        )



        print(
            f"\n===== {year}년 경제 순위 ====="
        )



        rank = 1



        for country, value in result:


            print(
                f"{rank}위 {country} : {value:,}"
            )


            rank += 1
          # chart.py
# 경제 데이터 시각화 시스템
# GDP / 무역량 변화 그래프 출력


import matplotlib.pyplot as plt





class ChartSystem:



    def __init__(self):

        pass





    def trade_chart(self, country, data):


        if country not in data:

            print("데이터 없음")

            return



        years = list(
            data[country].keys()
        )


        values = list(
            data[country].values()
        )



        plt.figure(
            figsize=(10,5)
        )



        plt.plot(
            years,
            values,
            marker="o"
        )



        plt.title(
            f"{country} 무역 규모 변화"
        )


        plt.xlabel(
            "Year"
        )


        plt.ylabel(
            "Trade (Billion USD)"
        )


        plt.grid()



        plt.show()






    def compare_chart(self, countries, data):


        plt.figure(
            figsize=(10,5)
        )



        for country in countries:


            if country in data:


                years = list(
                    data[country].keys()
                )


                values = list(
                    data[country].values()
                )



                plt.plot(

                    years,

                    values,

                    marker="o",

                    label=country

                )



        plt.title(
            "국가별 무역 성장 비교"
        )


        plt.xlabel(
            "Year"
        )


        plt.ylabel(
            "Trade"
        )


        plt.legend()


        plt.grid()



        plt.show()





    def bar_chart(self, ranking):


        countries = []

        values = []



        for country, value in ranking:


            countries.append(country)

            values.append(value)



        plt.figure(
            figsize=(10,5)
        )



        plt.bar(
            countries,
            values
        )



        plt.title(
            "국가 경제 순위"
        )


        plt.xlabel(
            "Country"
        )


        plt.ylabel(
            "Value"
        )



        plt.xticks(
            rotation=45
        )



        plt.show()
      # world_news.py
# 국제 뉴스 기반 경제 이벤트 시스템
# 실제 경제 상황처럼 뉴스 발생


import random



class WorldNewsSystem:


    def __init__(self, market):

        self.market = market



        self.news = [


            {
                "title": "미국 금리 인상 발표",
                "effect": {
                    "자동차": -2000,
                    "석유": -1000
                }
            },


            {
                "title": "중국 경기 부양책 발표",
                "effect": {
                    "반도체": 5000,
                    "자동차": 3000
                }
            },


            {
                "title": "유럽 친환경 규제 강화",
                "effect": {
                    "배터리": 7000,
                    "석유": -4000
                }
            },


            {
                "title": "글로벌 반도체 수요 증가",
                "effect": {
                    "반도체": 10000
                }
            },


            {
                "title": "국제 원자재 가격 폭등",
                "effect": {
                    "석유": 8000,
                    "농산물": 4000
                }
            },


            {
                "title": "세계 무역 협력 확대",
                "effect": {
                    "반도체": 3000,
                    "자동차": 3000,
                    "배터리": 3000
                }
            },


            {
                "title": "해상 운송 비용 증가",
                "effect": {
                    "자동차": -3000,
                    "농산물": -2000
                }
            }


        ]





    def generate_news(self):


        news = random.choice(
            self.news
        )


        print("\n📰 WORLD ECONOMIC NEWS")
        print("----------------------")

        print(
            news["title"]
        )


        for product, value in news["effect"].items():


            self.market.change_price(
                product,
                value
            )


            if value > 0:

                print(
                    f"{product} 가격 상승 +{value:,}원"
                )

            else:

                print(
                    f"{product} 가격 하락 {value:,}원"
                )





    def add_custom_news(self, title, product, value):


        self.news.append(

            {

                "title": title,

                "effect": {

                    product: value

                }

            }

        )


        print(
            "새로운 경제 뉴스 추가 완료"
        )
      # game_engine.py
# 전체 게임 시스템 통합 엔진


from market import Market
from trade import TradeSystem
from event import EventSystem
from world_news import WorldNewsSystem
from finance import FinanceSystem
from company import CompanySystem
from technology import TechnologySystem
from government import GovernmentSystem
from ai_country import AICountrySystem
from achievement import AchievementSystem





class GameEngine:



    def __init__(self):


        self.market = Market()

        self.trade = TradeSystem(
            self.market
        )

        self.event = EventSystem(
            self.market
        )

        self.news = WorldNewsSystem(
            self.market
        )

        self.finance = FinanceSystem()

        self.company = CompanySystem()

        self.tech = TechnologySystem()

        self.gov = GovernmentSystem()

        self.ai = AICountrySystem()

        self.achievement = AchievementSystem()



        self.money = 1000000

        self.turn = 1





    def next_turn(self):


        print(
            f"\n===== TURN {self.turn} ====="
        )


        self.turn += 1


        # AI 국가 행동

        self.ai.ai_turn()



        # 세계 뉴스 발생 확률

        import random


        if random.randint(1,3)==1:

            self.news.generate_news()



        # 시장 변화

        print(
            "🌎 세계 시장 변화"
        )



    def menu(self):


        while True:


            print("""
===========================
🌎 GLOBAL TRADE SIMULATOR
===========================

1. 시장 보기
2. 무역 거래
3. 금융 관리
4. 기업 운영
5. 기술 개발
6. 정부 정책
7. 세계 이벤트
8. AI 국가 현황
9. 턴 진행
0. 종료

===========================
""")


            command = input("> ")



            if command=="1":

                self.market.show_products()



            elif command=="2":

                print("""
1. 구매
2. 판매
""")

                c=input("> ")


                if c=="1":

                    self.money=self.trade.buy(
                        "",
                        self.money
                    )

                else:

                    self.money=self.trade.sell(
                        "",
                        self.money
                    )





            elif command=="3":

                print("""
1. 대출
2. 상환
3. 투자
4. 투자 결과
""")

                c=input("> ")



                if c=="1":

                    self.money=self.finance.borrow(
                        self.money
                    )


                elif c=="2":

                    self.money=self.finance.repay(
                        self.money
                    )


                elif c=="3":

                    self.money=self.finance.invest(
                        self.money
                    )


                elif c=="4":

                    self.money=self.finance.market_result(
                        self.money
                    )






            elif command=="4":


                print("""
1. 기업 설립
2. 고용
3. 생산
4. 수출
5. 기업 현황
""")


                c=input("> ")



                if c=="1":

                    self.company.create_company()


                elif c=="2":

                    self.company.hire()


                elif c=="3":

                    self.company.produce()


                elif c=="4":

                    self.company.export(
                        self.market
                    )


                elif c=="5":

                    self.company.status()





            elif command=="5":

                print("""
1. 연구 투자
2. 기술 개발
3. 기술 확인
""")


                c=input("> ")


                if c=="1":

                    self.money=self.tech.invest_research(
                        self.money
                    )


                elif c=="2":

                    self.tech.develop()


                else:

                    self.tech.show()





            elif command=="6":

                self.gov.show_policy()



            elif command=="7":

                self.event.random_event()



            elif command=="8":

                self.ai.ranking()



            elif command=="9":

                self.next_turn()



            elif command=="0":

                print("게임 종료")

                break



            else:

                print("잘못된 입력")
              # run.py
# 게임 실행 파일


from game_engine import GameEngine




def main():


    print("""
=================================

🌎 GLOBAL TRADE SIMULATOR

세계 무역 경영 시뮬레이션

=================================
""")


    game = GameEngine()


    game.menu()





if __name__ == "__main__":

    main()
        return self.products[product]["price"]
