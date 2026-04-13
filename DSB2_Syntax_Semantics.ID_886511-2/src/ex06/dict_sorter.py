list_of_tuples = [
    ('Russia', '25'),
    ('France', '132'),
    ('Germany', '132'),
    ('Spain', '178'),
    ('Italy', '162'),
    ('Portugal', '17'),
    ('Finland', '3'),
    ('Hungary', '2'),
    ('The Netherlands', '28'),
    ('The USA', '610'),
    ('The United Kingdom', '95'),
    ('China', '83'),
    ('Iran', '76'),
    ('Turkey', '65'),
    ('Belgium', '34'),
    ('Canada', '28'),
    ('Switzerland', '26'),
    ('Brazil', '25'),
    ('Austria', '14'),
    ('Israel', '12')
]

def to_dictionary():
    dictionary = {}
    for country, value in list_of_tuples:
        dictionary[country] = value
    dictionary = sort_dict(dictionary)
    for country, value in dictionary.items():
        print(country)

def sort_dict(dictionary):
    sorted_dictionary = dict(sorted(dictionary.items(), 
                             key=lambda kv: (-int(kv[1]), kv[0])))
    return sorted_dictionary

if __name__ == '__main__':
    to_dictionary()
        