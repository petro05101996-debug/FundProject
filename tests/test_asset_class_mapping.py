from investment_lab.domain.models import normalize_asset_class


def test_asset_class_aliases():
    assert normalize_asset_class('Акции РФ') == 'Акции'
    assert normalize_asset_class('акции рф') == 'Акции'
    assert normalize_asset_class('Облигации РФ') == 'Облигации'
    assert normalize_asset_class('Фонд денежного рынка') == 'Денежные средства'
    assert normalize_asset_class('ОФЗ') == 'Облигации'
    assert normalize_asset_class('Корпоративная облигация') == 'Облигации'
    assert normalize_asset_class('Накопительный счёт') == 'Денежные средства'
    assert normalize_asset_class('Золото') == 'Товары'
    assert normalize_asset_class('REIT') == 'Недвижимость'
    assert normalize_asset_class('Непонятный актив') == 'Альтернативные'
