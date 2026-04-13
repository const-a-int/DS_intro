import pytest
import sys
import os
from financial_enhanced import *

sys.path.append(os.path.dirname(__file__))

class TestFinancial:
    
    def test_input_data_valid(self):
        """Тест корректного ввода данных"""
        # Эмулируем sys.argv
        sys.argv = ['financial.py', 'MSFT', 'Total Revenue']
        ticker, field = input_data()
        assert ticker == 'MSFT'
        assert field == 'Total Revenue'
    
    def test_input_data_with_quotes(self):
        """Тест ввода данных с кавычками"""
        sys.argv = ['financial.py', "'MSFT'", "'Total Revenue'"]
        ticker, field = input_data()
        assert ticker == 'MSFT'
        assert field == 'Total Revenue'
    
    def test_input_data_wrong_args(self):
        """Тест неправильного количества аргументов"""
        sys.argv = ['financial.py', 'MSFT']  # Только один аргумент
        with pytest.raises(SystemExit):
            input_data()
    
    def test_send_request_valid_url(self):
        """Тест корректного URL"""
        url = 'https://finance.yahoo.com/quote/MSFT/financials/'
        answer = send_request(url)
        assert answer.status_code == 200
    
    def test_send_request_invalid_url(self):
        """Тест некорректного URL"""
        url = 'https://finance.yahoo.com/quote/INVALIDTICKER123/financials/'
        with pytest.raises(Exception, match="Page not found"):
            send_request(url)
    
    def test_parsing_page_valid_field(self):
        """Тест парсинга существующего поля"""
        # Сначала получаем реальную страницу
        url = 'https://finance.yahoo.com/quote/MSFT/financials/'
        answer = send_request(url)
        
        result = parsing_page(answer, 'Total Revenue')
        expected_values = ('Total Revenue', '281,724,000', '281,724,000', '245,122,000', '211,915,000', '198,270,000')
        assert result == expected_values
    
    def test_parsing_page_invalid_field(self):
        """Тест парсинга несуществующего поля"""
        url = 'https://finance.yahoo.com/quote/MSFT/financials/'
        answer = send_request(url)
        
        with pytest.raises(Exception, match="Field 'Invalid Field' not found"):
            parsing_page(answer, 'Invalid Field')
    
    def test_integration_valid(self):
        """Интеграционный тест - полный поток"""
        # Эмулируем полный вызов
        sys.argv = ['financial.py', 'MSFT', 'Total Revenue']
        ticker, field = input_data()
        url = f'https://finance.yahoo.com/quote/{ticker}/financials/'
        answer = send_request(url)
        result = parsing_page(answer, field)

        expected_values = ('Total Revenue', '281,724,000', '281,724,000', '245,122,000', '211,915,000', '198,270,000')
        assert result == expected_values
    
    def test_integration_invalid_ticker(self):
        """Тест невалидного тикера"""
        sys.argv = ['financial.py', 'INVALID123', 'Total Revenue']
        ticker, field = input_data()
        url = f'https://finance.yahoo.com/quote/{ticker}/financials/'
        
        with pytest.raises(Exception, match="Page not found"):
            send_request(url)

    def test_return_type_is_tuple(self):
        """Тест что возвращаемый тип - кортеж"""
        url = 'https://finance.yahoo.com/quote/MSFT/financials/'
        answer = send_request(url)
        result = parsing_page(answer, 'Total Revenue')
        
        assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"

if __name__ == '__main__':
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])