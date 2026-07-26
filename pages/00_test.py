# run.py
import random

# ----------------------------------------------------
# Market System
# ----------------------------------------------------
class Market:
    def __init__(self):
        self.countries = {
            "중국": {"GDP": 18000, "export": 3500},
            "미국": {"GDP": 28000, "export": 2000},
            "한국": {"GDP": 1800, "export": 700},
            "일본": {"GDP": 4200, "export": 900},
            "독일": {"GDP": 4500, "export": 1700},
            "네덜란드": {"GDP": 1100, "export": 900}
        }
        self.products = {
            "반도체": {"price": 10000, "demand": 90},
            "자동차": {"price": 30000, "demand": 70},
            "석유": {"price": 5000, "demand": 80},
            "농산물": {"price": 3000, "demand": 60},
            "배터리": {"price": 15000, "demand": 85}
        }

    def show_products(self):
        print("\n===== 현재 시장 =====")
        for name, data in self.products.items():
            print(f"{name} | 가격: {data['price']:,}원 | 수요: {data['demand']}%")

    def change_price(self, product, value):
        if product in self.products:
            self.products[product]["price"] += value
            if self.products[product]["price"] < 100:
                self.products[product]["price"] = 100

    def get_price(self, product):
        if product in self.products:
            return self.products[product]["price"]
        return 0


# ----------------------------------------------------
# Trade System
# ----------------------------------------------------
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
        try:
            amount = int(input("구매 수량: "))
        except ValueError:
            print("숫자를 입력해주세요.")
            return money

        cost = price * amount
        if money < cost:
            print("자금 부족")
            return money

        money -= cost
        self.inventory[product] = self.inventory.get(product, 0) + amount
        print(f"{product} {amount}개 구매 완료")
        return money

    def sell(self, country, money):
        if not self.inventory:
            print("판매할 상품 없음")
            return money

        print("\n보유 상품")
        for item, amount in self.inventory.items():
            print(f"{item}: {amount}개")

        product = input("판매할 상품: ")
        if product not in self.inventory or self.inventory[product] <= 0:
            print("보유하지 않은 상품")
            return money

        try:
            amount = int(input("판매 수량: "))
        except ValueError:
            print("숫자를 입력해주세요.")
            return money

        if amount > self.inventory[product]:
            print("수량 부족")
            return money

        price = self.market.get_price(product)
        income = price * amount
        money += income
        self.inventory[product] -= amount
        print(f"{product} {amount}개 판매 +{income:,}원")
        return money


# ----------------------------------------------------
# Event & News
# ----------------------------------------------------
class EventSystem:
    def __init__(self, market):
        self.market = market
        self.events = [
            {"name": "세계 반도체 부족 발생", "effect": {"반도체": 5000}},
            {"name": "국제 유가 상승", "effect": {"석유": 3000}},
            {"name": "세계 경기 침체", "effect": {"자동차": -5000, "농산물": 1000}},
            {"name": "친환경 산업 성장", "effect": {"배터리": 4000}},
            {"name": "무역 갈등 발생", "effect": {"반도체": -3000, "자동차": -2000}}
        ]

    def random_event(self):
        event = random.choice(self.events)
        print("\n🌍 세계 이벤트 발생!")
        print(event["name"])
        for product, change in event["effect"].items():
            self.market.change_price(product, change)
            print(f"{product} 가격 {'상승 +' if change > 0 else '하락 '}{change:,}원")


class WorldNewsSystem:
    def __init__(self, market):
        self.market = market
        self.news = [
            {"title": "미국 금리 인상 발표", "effect": {"자동차": -2000, "석유": -1000}},
            {"title": "중국 경기 부양책 발표", "effect": {"반도체": 5000, "자동차": 3000}},
            {"title": "유럽 친환경 규제 강화", "effect": {"배터리": 7000, "석유": -4000}},
            {"title": "글로벌 반도체 수요 증가", "effect": {"반도체": 10000}}
        ]

    def generate_news(self):
        news = random.choice(self.news)
        print("\n📰 WORLD ECONOMIC NEWS")
        print("----------------------")
        print(news["title"])
        for product, value in news["effect"].items():
            self.market.change_price(product, value)
            print(f"{product} 가격 {'상승 +' if value > 0 else '하락 '}{value:,}원")


# ----------------------------------------------------
# Finance / Company / Tech / Govt / AI Systems
# ----------------------------------------------------
class FinanceSystem:
    def __init__(self):
        self.loan = 0
        self.investment = 0

    def borrow(self, money):
        amount = int(input("대출 금액 입력: "))
        self.loan += amount
        money += amount
        print(f"{amount:,}원 대출 완료 (부채: {self.loan:,}원)")
        return money

    def repay(self, money):
        if self.loan == 0:
            print("갚을 대출 없음")
            return money
        amount = int(input("상환 금액 입력: "))
        if amount > money:
            print("자금 부족")
            return money
        amount = min(amount, self.loan)
        money -= amount
        self.loan -= amount
        print(f"{amount:,}원 상환 완료")
        return money

    def invest(self, money):
        amount = int(input("투자 금액 입력: "))
        if amount > money:
            print("투자 불가능")
            return money
        self.investment += amount
        money -= amount
        print(f"{amount:,}원 투자 완료")
        return money

    def market_result(self, money):
        if self.investment == 0:
            print("투자 내역 없음")
            return money
        rate = random.randint(-20, 30)
        result = int(self.investment * (1 + rate / 100))
        money += result
        print(f"투자 결과: {rate}% -> {result:,}원 회수")
        self.investment = 0
        return money


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
        print(f"{name} 설립 완료! (초기 자본: 500,000원)")

    def hire(self):
        if not self.company:
            print("기업이 없습니다")
            return
        count = int(input("고용할 직원 수: "))
        cost = count * 10000
        if cost > self.money:
            print("자금 부족")
            return
        self.money -= cost
        self.workers += count
        print(f"{count}명 고용 완료")

    def produce(self):
        if self.workers == 0:
            print("직원이 없습니다")
            return
        print("\n1. 반도체\n2. 자동차\n3. 배터리\n4. 농산물")
        choice = input("제품 선택: ")
        products = {"1": "반도체", "2": "자동차", "3": "배터리", "4": "농산물"}
        if choice not in products:
            print("잘못 입력")
            return
        product = products[choice]
        amount = self.workers * 10
        self.production[product] = self.production.get(product, 0) + amount
        print(f"{product} {amount}개 생산")

    def export(self, market):
        if not self.production:
            print("수출할 제품 없음")
            return
        print("\n보유 제품:", self.production)
        product = input("수출 제품: ")
        if product not in self.production or self.production[product] <= 0:
            print("제품 없음")
            return
        amount = self.production[product]
        price = market.get_price(product)
        income = amount * price
        self.money += income
        self.production[product] = 0
        print(f"{product} 수출 성공 (+{income:,}원)")

    def status(self):
        print(f"\n===== 기업 현황 =====\n기업: {self.company}\n자금: {self.money:,}원\n직원: {self.workers}명\n생산: {self.production}")


class TechnologySystem:
    def __init__(self):
        self.tech_level = {"반도체": 1, "자동차": 1, "배터리": 1, "AI": 1, "친환경": 1}
        self.research_point = 0

    def invest_research(self, money):
        cost = int(input("연구 투자 금액: "))
        if cost > money:
            print("자금 부족")
            return money
        money -= cost
        gained = cost // 10000
        self.research_point += gained
        print(f"연구 포인트 +{gained}")
        return money

    def develop(self):
        print("\n개발 가능한 기술:", self.tech_level)
        target = input("개발할 기술: ")
        if target not in self.tech_level:
            print("없는 기술")
            return
        needed = self.tech_level[target] * 10
        if self.research_point < needed:
            print("연구 포인트 부족")
            return
        self.research_point -= needed
        self.tech_level[target] += 1
        print(f"{target} 기술 발전! 현재 Lv.{self.tech_level[target]}")

    def show(self):
        print(f"\n===== 🔬 기술 현황 =====\n기술: {self.tech_level}\n연구 포인트: {self.research_point}")


class GovernmentSystem:
    def __init__(self):
        self.policy = {"tax": 10, "interest": 3, "subsidy": 0, "currency": 100}

    def show_policy(self):
        print(f"\n===== 🏛 정부 정책 =====\n세율: {self.policy['tax']}%\n금리: {self.policy['interest']}%\n보조금: {self.policy['subsidy']:,}원")


class AICountrySystem:
    def __init__(self):
        self.countries = {
            "미국": {"money": 5000000, "industry": 90, "export": 100},
            "중국": {"money": 4500000, "industry": 95, "export": 120},
            "독일": {"money": 3000000, "industry": 85, "export": 90},
            "일본": {"money": 2800000, "industry": 80, "export": 80},
            "한국": {"money": 2000000, "industry": 85, "export": 70},
            "네덜란드": {"money": 1500000, "industry": 75, "export": 85}
        }

    def ai_turn(self):
        print("\n🤖 AI 국가 행동")
        for country, data in self.countries.items():
            action = random.choice(["produce", "trade", "research"])
            if action == "produce":
                profit = data["industry"] * 10000
                data["money"] += profit
                data["export"] += 1
                print(f"{country}: 생산 확대 +{profit:,}원")
            elif action == "trade":
                profit = random.randint(10000, 100000)
                data["money"] += profit
                data["export"] += 2
                print(f"{country}: 무역 성공 +{profit:,}원")
            else:
                data["industry"] += 1
                print(f"{country}: 기술 투자 산업력 증가")

    def ranking(self):
        print("\n===== 🌎 세계 경제 순위 =====")
        ranking = sorted(self.countries.items(), key=lambda x: x[1]["money"], reverse=True)
        for rank, (country, data) in enumerate(ranking, 1):
            print(f"{rank}위 {country} | 자본:{data['money']:,}원 | 수출:{data['export']}")


# ----------------------------------------------------
# Game Engine Main
# ----------------------------------------------------
class GameEngine:
    def __init__(self):
        self.market = Market()
        self.trade = TradeSystem(self.market)
        self.event = EventSystem(self.market)
        self.news = WorldNewsSystem(self.market)
        self.finance = FinanceSystem()
        self.company = CompanySystem()
        self.tech = TechnologySystem()
        self.gov = GovernmentSystem()
        self.ai = AICountrySystem()
        self.money = 1000000
        self.turn = 1

    def next_turn(self):
        print(f"\n===== TURN {self.turn} =====")
        self.turn += 1
        self.ai.ai_turn()
        if random.randint(1, 3) == 1:
            self.news.generate_news()

    def menu(self):
        while True:
            print(f"""
===========================
🌎 GLOBAL TRADE SIMULATOR
현재 자금: {self.money:,}원
===========================
1. 시장 보기      2. 무역 거래
3. 금융 관리      4. 기업 운영
5. 기술 개발      6. 정부 정책
7. 세계 이벤트    8. AI 국가 현황
9. 턴 진행        0. 종료
===========================
""")
            command = input("> ")
            if command == "1":
                self.market.show_products()
            elif command == "2":
                c = input("1. 구매 | 2. 판매 > ")
                if c == "1":
                    self.money = self.trade.buy("", self.money)
                elif c == "2":
                    self.money = self.trade.sell("", self.money)
            elif command == "3":
                c = input("1. 대출 | 2. 상환 | 3. 투자 | 4. 투자 결과 > ")
                if c == "1":
                    self.money = self.finance.borrow(self.money)
                elif c == "2":
                    self.money = self.finance.repay(self.money)
                elif c == "3":
                    self.money = self.finance.invest(self.money)
                elif c == "4":
                    self.money = self.finance.market_result(self.money)
            elif command == "4":
                c = input("1. 설립 | 2. 고용 | 3. 생산 | 4. 수출 | 5. 현황 > ")
                if c == "1":
                    self.company.create_company()
                elif c == "2":
                    self.company.hire()
                elif c == "3":
                    self.company.produce()
                elif c == "4":
                    self.company.export(self.market)
                elif c == "5":
                    self.company.status()
            elif command == "5":
                c = input("1. 연구 투자 | 2. 기술 개발 | 3. 기술 확인 > ")
                if c == "1":
                    self.money = self.tech.invest_research(self.money)
                elif c == "2":
                    self.tech.develop()
                elif c == "3":
                    self.tech.show()
            elif command == "6":
                self.gov.show_policy()
            elif command == "7":
                self.event.random_event()
            elif command == "8":
                self.ai.ranking()
            elif command == "9":
                self.next_turn()
            elif command == "0":
                print("게임 종료")
                break
            else:
                print("잘못된 입력입니다.")

if __name__ == "__main__":
    game = GameEngine()
    game.menu()
