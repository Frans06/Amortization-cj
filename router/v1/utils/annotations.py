from apistar import types, validators

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
