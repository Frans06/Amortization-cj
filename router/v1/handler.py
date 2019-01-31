from .utils.amortization import french_method, german_method, american_method
from .utils.annotations import AmortizationTableRequest, AmortizationTableResponse

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
