# -*- coding: utf-8 -*-

# Temporal expresions
months = "(?P<month>enero|febrero|marzo|abril|mayo|junio|julio|agosto|sep?tiembre|octubre|noviembre|diciembre)"
numbers = "(?P<number>uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez| \
          once|doce|trece|catorce|quince|dieciseis|diecisiete| \
          dieciocho|diecinueve|veinte|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta| \
          noventa|cien)"
millions = "(?P<millions>mil|miles|millón|millon|millones|cientos|cien)"
modifiers = "(?P<modifier>anteúltim(o|a)|penúltim(o|a)|(ú|u)ltimo|(ú|u)ltimos|(ú|u)ltimas|(ú|u)ltima)"    
enumerators = "(?P<enumerator>primer(a|as|o|os)?|segund[oa]|tercer[oa]?|cuart[oa]|quint[oa]|sext[oa]|s(e|é)ptim[oa]|octav[oa]|noven[oa]|d[eé]cim[oa]|onceav[oa]|doceav[oa])"
periods = "(?P<period>días?|semanas?|meses|mes|bimestre|trimestre|cuatrimestre|semestre|años?)"
ades = "(?P<ades>antes|después)"
before = "(?P<before>est(as|a|e|os)|anterior|anteriores|pasad[ao]s?)"
after = "(?P<after>próxim(a|as|o|os)|siguientes)"
temp = "(?P<temp>acá|ahora|hoy|ayer|mañana)"
years = "(?P<year>\d{4}|(?<=\s)\d{4}|^\d{4})"
two_digits = "(?P<time_unit>\d{1,2})"
four_digits = "(?P<time_unit>\d{1,4})"

temporal_regex = [
	# dias, meses, años
	two_digits + "\sde\s" + months, # 12 de abril
    months  + "\sde\s" + years , # enero de 2014
    months, #enero, febrero
    years,# 2014, 1998
    numbers,
    modifiers,
    enumerators,
    periods,
    ades,
    before,
    after,
    temp,
    years,
    two_digits,
    four_digits,
    millions
]

# Measures
signs = "(?P<sign>(\$|US\$))"
currency = "(?P<currency>pesos|dólar|dolar|dolares|dólares)"

multiplicadores = "(?P<multiplier>(duplic|triplic|cuadruplic)(ar|o|ó|aron|ado)|doble|triple|cu[aá]druple|quintuple)"
divisores = "(?P<divider>mitad(es)?|tercios?|cuartos?|quintos?)"
comparadores = "(?P<compare>mayor|menor|igual|lo mismo|mejor|peor)"

maxmin = "(?P<maxmin>mínimo|máximo|mayoría|minoría)"
masmenos = "(?P<masmenos>m(a|á)s|menos)"
cantidades = "(?P<amount>todos|algunos|casi todos|ninguno)"

measure_regex = [
    signs,
    currency,
    multiplicadores,
    divisores,
    maxmin,
    masmenos,
    cantidades
]