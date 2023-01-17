from project import acro, abbrevSpell, miscChecks, breakDownMain, breakDownAcro, doubleCheck, createAbbrevList
import pytest


def test_breakDownMain():
    # Test with simply spaces:
    assert breakDownMain('Spaces test this   ') == ['Spaces', 'test', 'this']
    # Test with punctuation:
    assert breakDownMain('Test! with--punctuation?  ') == ['Test', 'with', 'punctuation']
    # Test full complicated bullets:
    assert breakDownMain('- This is a sample bullet; it is good/bad--it has stuff    ') == ['This', 'is', 'a', 'sample', 'bullet', 'it', 'is', 'good', 'bad', 'it', 'has', 'stuff']
    assert breakDownMain("- This is another!  we like this--help'd us") == ['This', 'is', 'another', 'we', 'like', 'this', "help'd", 'us']
    # Test full sentences:
    assert breakDownMain('We are testing. This sentance!') == ['We', 'are', 'testing', 'This', 'sentance']
    assert breakDownMain('I want test. Please, give me?') == ['I', 'want', 'test', 'Please', 'give', 'me']

def test_breakDownAcro():
    # Test with simple acronym additions:
    list = breakDownAcro('Spaces test this   here are-- some ACROS YES HAT DOG')
    checks = ['ACROS', 'YES', 'HAT', 'DOG']
    assert sorted(list) == sorted(checks)
    # Test with punctuation:
    list = breakDownAcro('Check on these acros--HEL FONT! ''RIDER?')
    checks = ['HEL', 'FONT', 'RIDER']  
    assert sorted(list) == sorted(checks)



def test_acro():
    # test with all acros
    itemsNotInAcros, itemsNotInText =  acro(['THIS', 'THAT', 'OTHER'], ['THIS', 'THAT', 'HELLO'])

    assert itemsNotInAcros == ['OTHER']
    assert itemsNotInText == ['HELLO']

    # test with mixed acros and text
    itemsNotInAcros, itemsNotInText = acro(['this', 'then', 'THAT', 'and', 'that', 'other', 'CBA', 'TIME', 'ABC'], ['THIS', 'THAT', 'HELLO', 'ABC'])

    assert sorted(itemsNotInAcros) == ['CBA', 'TIME']
    assert sorted(itemsNotInText) == ['HELLO', 'THIS']


def test_abbrevSpell():
    # this simply tests if abbrevSpell will detect misspelled words and ignore acronyms and approved abbreviations
    abbrevList = createAbbrevList()
    spellList = abbrevSpell(['this', 'will', 'test', 'Spellllling', 'and', 'ACROS', 'as', 'WeLl', 'fromeated', 'crs', 'trng', 'capt', 'ofcr'], abbrevList)
    assert 'spellllling' in spellList
    assert 'fromeated' in spellList
    assert 'capt' not in spellList
    assert 'ofcr' not in spellList
    assert 'this' not in spellList

def test_miscChecks():
    # test exclaimation
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('!  ')
    assert exclaimErr == False
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('! ')
    assert exclaimErr == True
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- Proclaim! This is not good.')
    assert exclaimErr == True
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- Proclaim!  This is good.')
    assert exclaimErr == False
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- Proclaim!   This is not good.')
    assert exclaimErr == True

    # test double hyphens for spaces
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- This test--is fine')
    assert doubleHyphErr == False
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- This test-- is not fine')
    assert doubleHyphErr == True
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- This test --is not fine')
    assert doubleHyphErr == True
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- This test -- is not fine')
    assert doubleHyphErr == True
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- This test  --is not fine')
    assert doubleHyphErr == True
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- This test--  is not fine')
    assert doubleHyphErr == True

    # test starting hyphens for one space after
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('- This test--is fine')
    assert startHyphErr == False
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('-This test--is not fine')
    assert startHyphErr == True
    exclaimErr, doubleHyphErr, startHyphErr = miscChecks('-  This test--is not fine')
    assert startHyphErr == True

def test_doubleCheck():
    assert sorted(doubleCheck(['123','234','345','456','345','234','123'])) == ['123','234','345']
    assert sorted(doubleCheck(['12','23','34','23','12','23','12'])) == ['12','23']
    assert sorted(doubleCheck(['pie', 'cone', 'tree', 'cone', 'tree'])) == sorted(['cone', 'tree'])

   

# For testing errors if needed:
#def test_too_large():
    #with pytest.raises(ValueError):
        #convert('3/2')

