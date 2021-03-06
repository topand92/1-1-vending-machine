####################################################################################################
# consumer_module
####################################################################################################

from basic_module import *

####################################################################################################

dflt = { 0: 'dflt' } # default

s0 = str_c('재고 없음', 'R') # state
s1 = str_c('잔액 부족', 'R')
s2 = str_c('구매 가능', 'G')

####################################################################################################
# show: 판매 중인 상품과 거스름돈의 상태를 출력
####################################################################################################

# 상품의 상태를 문자열로 반환
def check_state(d, k, c): # key
    if c[0] == 'dflt':
        if d[k][2] == 0:
            return s0
        else:
            return s2

    else:
        if d[k][2] == 0:
            return s0
        elif c[0] < d[k][1]:
            return s1
        else:
            return s2

# 상품의 목록(번호, 상태, 가격, 이름)을 출력
def print_menu(d, c=dflt, a=False): # admin
    print('판매 중인 상품의 목록')
    print_l()

    for k in d: # key
        print(str(k)+'번\t'+check_state(d, k, c)+'\t'+str(d[k][1])+'원\t'+d[k][0])
        if a == True:
            print('\t('+str(d[k][2])+'/10개)')
    print_l()

# 거스름돈의 재고 상태를 확인하고 출력
def print_change(c):
    for i in (100, 500, 1000):
        if c[i][0] < 10:
            print_c('현재 거스름돈이 부족합니다. 상품을 판매할 수 없습니다.', 'R')
            print_l()
            return False

    print_c('현재 거스름돈이 충분합니다. 상품을 구매할 수 있습니다.', 'G')
    print_l()

####################################################################################################
# insert_cash: 돈을 투입받음
####################################################################################################

# 돈을 투입받고, 세서 저장하고, 결과를 출력하는 함수
def input_cash(c):
    for i in (100, 500, 1000):
        # insert_cash: 돈을 인서트 슬롯에 투입
        c[i][1] = input_rng('투입할 '+str(i)+'원의 개수')
        # count_cash: 투입받은 돈을 세서 밸런스 슬롯에 저장
        c[0] += i * c[i][1]
        # stack_cash: 투입받은 돈을 스택시키고 인서트 슬롯을 초기화
        c[i][0] += c[i][1]
        c[i][1] = 0
    print_l()

    print_c('투입된 금액: '+str(c[0])+'원', 'B')
    print_l()

####################################################################################################
# buy: 구매할 상품을 선택하고, 결제 진행
####################################################################################################

# 구매할 상품의 키를 입력하는 루프, 선택한 키를 반환
def input_key(d, c):
    k = input_rng('구매할 상품의 번호', 1, max(d)) # key
    while True:
        if check_state(d, k, c) != s2:
            print(check_state(d, k, c)+'의 이유로 구매할 수 없는 상품입니다. 다시 입력해주세요.')
            k = input_rng('구매할 상품의 번호', 1, max(d))

        else:
            print_l()
            return k

# 결제 진행
def pay(d, k, c):
    p = d[k][1] # price
    print_c('선택하신 '+d[k][0]+' 음료의 가격은 '+str(p)+'원 입니다.', 'B')
    print_c('현재 잔액 '+str(c[0])+'원에서 음료 가격 '+str(p)+'원을 결제합니다.', 'R')
    c[0] -= p
    print_c('결제되었습니다. 남은 잔액은 '+str(c[0])+'원 입니다.', 'B')
    d[k][2] -= 1
    print_c(d[k][0]+' 음료가 투출되었습니다.', 'G')
    print_l()

####################################################################################################
# return_change: 잔액 반환
####################################################################################################

# 잔액 반환
def return_change(c):
    for i in (1000, 500, 100):
        # calc_change
        c[i][2] = c[0] // i
        c[0] = c[0] % i
        # return change
        print_c(str(i)+'원 '+str(c[i][2])+'개가 반환되었습니다.', 'G')
        # unstack_cash
        c[i][0] -= c[i][2]
        c[i][2] = 0
    print_l()