'''
Amortization Code
Simple apistar framework to calculate amortization on credit
'''
from apistar import App, Route, types, validators

class AmortizationTableRequest(types.Type):
    '''
    Annotation for AmortizationTableRequest
    '''
    methods = ['french', 'german', 'american']
    principal = validators.Number()
    interest_rate = validators.Number()
    duration_months = validators.Integer()
    method = validators.String(enum=methods)

class AmortizationPayment(types.Type):
    '''
    Annotation for AmortizationPayment
    '''
    period = validators.Integer()
    amount = validators.Number()
    interest = validators.Number()
    principal = validators.Number()
    principal_balance = validators.Number()

class AmortizationTableResponse(types.Type):
    '''
    Annotation for AmortizationTableResponse
    '''
    method = validators.String()
    payments = validators.Array(items=AmortizationPayment)

def fixed_rate_payment(p: float, i: float, n: int) -> float:
    '''
    calculate Month payment
    '''
    rate = i/12
    return p * (rate / ((1 - (1 + rate) ** -n)))

def french_method(request) -> list:
    '''
    French method to calculate payments
    '''
    payments = []
    montly_payment = fixed_rate_payment(request.principal,
                                        request.interest_rate,
                                        request.duration_months)
    for period in range(request.duration_months+1):
        if period == 0:
            payments.append(AmortizationPayment(period=0, amount=0, interest=0, principal=0,
                                                principal_balance=request.principal))
        else:
            last_payment = payments[period - 1]
            interest = last_payment.principal_balance * (request.interest_rate / 12)
            principal = montly_payment - interest
            principal_balance = last_payment.principal_balance - principal

            payment = AmortizationPayment(period=period,
                                          amount=montly_payment,
                                          interest=interest,
                                          principal=principal,
                                          principal_balance=principal_balance)

            payments.append(payment)
    return payments

def german_method(request) -> list:
    '''
    German method to calculate payments
    '''
    payments = []
    amortization = request.principal/request.duration_months

    for period in range(request.duration_months+1):
        if period == 0:
            payments.append(AmortizationPayment(period=0, amount=0, interest=0, principal=0,
                                                principal_balance=request.principal))
        else:
            last_payment = payments[period - 1]
            interest = (last_payment.principal_balance) * (request.interest_rate / 12)
            principal = amortization
            montly_payment = principal + interest
            principal_balance = last_payment.principal_balance - principal

            payment = AmortizationPayment(period=period,
                                          amount=montly_payment,
                                          interest=interest,
                                          principal=principal,
                                          principal_balance=principal_balance)

            payments.append(payment)
    return payments

def american_method(request) -> list:
    '''
    American method to calculate payments
    '''
    payments = []
    interest_monthtly = request.interest_rate/12
    montly_payment = request.principal * interest_monthtly
    interest = montly_payment
    for period in range(request.duration_months+1):
        if period == 0:
            payments.append(AmortizationPayment(period=0, amount=0, interest=0, principal=0,
                                                principal_balance=0))
        elif period == request.duration_months:
            payments.append(AmortizationPayment(period=period,
                                                amount=request.principal*(1+interest_monthtly),
                                                interest=interest,
                                                principal=request.principal,
                                                principal_balance=request.principal))
        else:
            last_payment = payments[period - 1]
            principal = 0
            principal_balance = last_payment.principal_balance - principal

            payment = AmortizationPayment(period=period,
                                          amount=montly_payment,
                                          interest=interest,
                                          principal=principal,
                                          principal_balance=principal_balance)

            payments.append(payment)
    return payments

def amortization_table_handler(request: AmortizationTableRequest) -> AmortizationTableResponse:
    '''
    Handling request and formulate table
    '''

    durations_months = [12, 24, 36, 48]
    if request.duration_months not in durations_months:
        response = {"duration_months": "Must be one of [12, 24, 36, 48]."}
        return response

    if request.method == 'french':
        payments = french_method(request)
    if request.method == 'german':
        payments = german_method(request)
    if request.method == 'american':
        payments = american_method(request)

    payments_shower = [{key:round(value, 2) for key, value in payment.items()}
                       for payment in payments]
    response = AmortizationTableResponse(method=request.method,
                                         payments=payments_shower)
    return response


routes = [
    Route('/amortization-table', method='POST', handler=amortization_table_handler),
]


app = App(routes=routes)

if __name__ == '__main__':
    app.serve('0.0.0.0', 4500, debug=True)
