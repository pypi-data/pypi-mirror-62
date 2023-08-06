import csvmatch

def test_simple():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway'],
        ['William Shakespeare']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2)
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'William Shakespeare']
    ]

def test_fields():
    headers1 = ['name', 'born']
    data1 = [
        ['William Shakespeare', '1564'],
        ['Christopher Marlowe', '1583']
    ]
    headers2 = ['person', 'birth']
    data2 = [
        ['Christopher Marlowe', 'unknown'],
        ['William Shakespeare', '1564']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2)
    assert keys == ['name', 'born', 'person', 'birth']
    assert results == [
        ['William Shakespeare', '1564', 'William Shakespeare', '1564']
    ]

def test_multiple():
    headers1 = ['name']
    data1 = [
        ['Anne Hathaway'],
        ['Anne Hathaway'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway'],
        ['Christopher Marlowe'],
        ['Christopher Marlowe']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2)
    assert keys == ['name', 'person']
    assert results == [
        ['Anne Hathaway', 'Anne Hathaway'],
        ['Anne Hathaway', 'Anne Hathaway'],
        ['Christopher Marlowe', 'Christopher Marlowe'],
        ['Christopher Marlowe', 'Christopher Marlowe']
    ]

def test_same_headers():
    headers1 = ['name']
    data1 = [
        ['Anne Hathaway'],
        ['Christopher Marlowe']
    ]
    headers2 = ['name']
    data2 = [
        ['William Shakespeare'],
        ['Christopher Marlowe']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2)
    assert keys == ['name', 'name']
    assert results == [
        ['Christopher Marlowe', 'Christopher Marlowe']
    ]

def test_fields():
    headers1 = ['name', 'born']
    data1 = [
        ['William Shakespeare', '1564'],
        ['Christopher Marlowe', '1564']
    ]
    headers2 = ['person', 'hometown']
    data2 = [
        ['William Shakespeare', 'Stratford-upon-Avon'],
        ['Anne Hathaway', 'Stratford-upon-Avon']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, fields1=['name'], fields2=['person'])
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'William Shakespeare']
    ]

def test_ordering():
    headers1 = ['name', 'born']
    data1 = [
        ['William Shakespeare', '1564'],
        ['Christopher Marlowe', '1564']
    ]
    headers2 = ['birth', 'person']
    data2 = [
        ['1564', 'William Shakespeare'],
        ['1556', 'Anne Hathaway']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, fields1=['name', 'born'], fields2=['person', 'birth'])
    assert keys == ['name', 'born', 'person', 'birth']
    assert results == [
        ['William Shakespeare', '1564', 'William Shakespeare', '1564']
    ]

def test_ignore_case():
    headers1 = ['name']
    data1 = [
        ['Anne Hathaway'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['william shakespeare'],
        ['christopher marlowe']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_case=True)
    assert keys == ['name', 'person']
    assert results == [
        ['Christopher Marlowe', 'christopher marlowe']
    ]

def test_ignore_custom():
    headers1 = ['name']
    data1 = [
        ['ONE Anne Hathaway'],
        ['TWO Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['THREE Christopher Marlowe'],
        ['FOUR William Shakespeare']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_custom=['ONE', 'TWO', 'THREE', 'FOUR'])
    assert keys == ['name', 'person']
    assert results == [
        ['TWO Christopher Marlowe', 'THREE Christopher Marlowe']
    ]

def test_ignore_titles():
    headers1 = ['name']
    data1 = [
        ['Ms. Anne Hathaway'],
        ['Mr. William Shakespeare']
    ]
    headers2 = ['person']
    data2 = [
        ['Mr. Christopher Marlowe'],
        ['Mrs. Anne Hathaway']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_titles=True)
    assert keys == ['name', 'person']
    assert results == [
        ['Ms. Anne Hathaway', 'Mrs. Anne Hathaway']
    ]

def test_ignore_nonlatin():
    headers1 = ['name']
    data1 = [
        ['Charlotte Brontë'],
        ['Gabriel García Márquez']
    ]
    headers2 = ['person']
    data2 = [
        ['Gabriel Garcia Marquez'],
        ['Leo Tolstoy']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_nonlatin=True)
    assert keys == ['name', 'person']
    assert results == [
        ['Gabriel García Márquez', 'Gabriel Garcia Marquez']
    ]

def test_ignore_nonalpha():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Anne-Hathaway'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway!'],
        ['William Shakespeare.']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_nonalpha=True)
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'William Shakespeare.'],
        ['Anne-Hathaway', 'Anne Hathaway!']
    ]

def test_ignore_order_words():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Anne Hathaway']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway'],
        ['Shakespeare William']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_order_words=True)
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'Shakespeare William'],
        ['Anne Hathaway', 'Anne Hathaway']
    ]

def test_ignore_order_letters():
    headers1 = ['name']
    data1 = [
        ['w ill iam shake speare'],
        ['judith quiney']
    ]
    headers2 = ['text']
    data2 = [
        ['i am a weakish speller'],
        ['something else']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_order_letters=True)
    assert keys == ['name', 'text']
    assert results == [
        ['w ill iam shake speare', 'i am a weakish speller']
    ]

def test_multiple_ignores1():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Charlotte Brontë']
    ]
    headers2 = ['person']
    data2 = [
        ['BRONTE, CHARLOTTE'],
        ['SHAKESPEARE, WILLIAM']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_case=True, ignore_nonlatin=True, ignore_nonalpha=True, ignore_order_words=True)
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'SHAKESPEARE, WILLIAM'],
        ['Charlotte Brontë', 'BRONTE, CHARLOTTE']
    ]

def test_multiple_ignores2():
    headers1 = ['name']
    data1 = [
        ['John Shakespeare'],
        ['Mary Árden']
    ]
    headers2 = ['person']
    data2 = [
        ['Arden, Mary'],
        ['Hathaway, Anne']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_nonlatin=True, ignore_nonalpha=True, ignore_order_words=True)
    assert keys == ['name', 'person']
    assert results == [
        ['Mary Árden', 'Arden, Mary']
    ]

def test_multiple_ignores3():
    headers1 = ['name']
    data1 = [
        ['E M Forster'],
        ['J D Salinger']
    ]
    headers2 = ['person']
    data2 = [
        ['H a r p e r, Lee'],
        ['F ó r s t e r, ÉM']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_nonlatin=True, ignore_nonalpha=True, ignore_order_letters=True)
    assert keys == ['name', 'person']
    assert results == [
        ['E M Forster', 'F ó r s t e r, ÉM']
    ]

def test_multiple_ignores4():
    headers1 = ['name']
    data1 = [
        ['Prof. William Shakespeare'],
        ['Ms Anne Hathaway']
    ]
    headers2 = ['person']
    data2 = [
        ['Pröf William Shakespeare'],
        ['Christopher Marlowe']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_nonlatin=True, ignore_titles=True)
    assert keys == ['name', 'person']
    assert results == [
        ['Prof. William Shakespeare', 'Pröf William Shakespeare']
    ]

def test_multiple_ignores5():
    headers1 = ['name']
    data1 = [
        ['William Shakéspeare'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway'],
        ['William Shakespeare']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, ignore_nonalpha=True, ignore_nonlatin=True)
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakéspeare', 'William Shakespeare']
    ]

def test_fuzzy_levenshtein():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Anne Hathaway']
    ]
    headers2 = ['person']
    data2 = [
        ['Ann Athawei'],
        ['Will Sheikhspere']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, methods=['levenshtein'])
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'Will Sheikhspere'],
        ['Anne Hathaway', 'Ann Athawei']
    ]

def test_fuzzy_levenshtein_fields():
    headers1 = ['name', 'address', 'born']
    data1 = [
        ['William Shakespeare', 'Henley Street', '1564'],
        ['Christopher Marlowe', 'Corpus Christi', '1564']
    ]
    headers2 = ['birth', 'person', 'location']
    data2 = [
        ['1564', 'Will Sheikhspere', 'Henley Street'],
        ['1556', 'Anne Hathaway', 'Cottage Lane']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, fields1=['name', 'address'], fields2=['person', 'location'], methods=['levenshtein'], output=['1.name', '1.address', '2.person', '2.location', 'degree'])
    assert keys == ['name', 'address', 'person', 'location', 'degree']
    assert results == [
        ['William Shakespeare', 'Henley Street', 'Will Sheikhspere', 'Henley Street', '0.8157894736842105']
    ]

def test_fuzzy_jaro():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Chris Barlow'],
        ['Willy Shake-Spear']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, methods=['jaro'])
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'Willy Shake-Spear'],
        ['Christopher Marlowe', 'Chris Barlow']
    ]

def test_fuzzy_metaphone():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Anne Hathaway']
    ]
    headers2 = ['person']
    data2 = [
        ['Ann Athawei'],
        ['Will Sheikhspere']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, methods=['metaphone'])
    assert keys == ['name', 'person']
    assert results == [
        ['Anne Hathaway', 'Ann Athawei']
    ]

def test_output():
    headers1 = ['name', 'born']
    data1 = [
        ['William Shakespeare', '1564'],
        ['Christopher Marlowe', '1583']
    ]
    headers2 = ['person', 'died']
    data2 = [
        ['Anne Hathaway', '1623'],
        ['William Shakespeare', '1616']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, fields1=['name'], fields2=['person'], output=['1*', '2.died', 'degree'])
    assert keys == ['name', 'born', 'died', 'degree']
    assert results == [
        ['William Shakespeare', '1564', '1616', '1.0']
    ]

def test_join_left_outer():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway'],
        ['William Shakespeare']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, join='left-outer')
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'William Shakespeare'],
        ['Christopher Marlowe', '']
    ]

def test_join_right_outer():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway'],
        ['William Shakespeare']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, join='right-outer')
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'William Shakespeare'],
        ['', 'Anne Hathaway']
    ]

def test_join_full_outer():
    headers1 = ['name']
    data1 = [
        ['William Shakespeare'],
        ['Christopher Marlowe']
    ]
    headers2 = ['person']
    data2 = [
        ['Anne Hathaway'],
        ['William Shakespeare']
    ]
    results, keys = csvmatch.run(data1, headers1, data2, headers2, join='full-outer')
    assert keys == ['name', 'person']
    assert results == [
        ['William Shakespeare', 'William Shakespeare'],
        ['Christopher Marlowe', ''],
        ['', 'Anne Hathaway']
    ]
