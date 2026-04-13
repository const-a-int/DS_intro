def data_types():
    int_ = 1
    str_ = 'a'
    float_ = 1.0
    bool_ = True
    list_ = [1, 2, 3]
    set_ = {1, 2, 3}
    tuple_= (1, 2, 3)
    dict_ = {"1":"two"}

    types = [type(data).__name__ for data in (int_,
                                          str_,
                                          float_,
                                          bool_,
                                          list_,
                                          set_,
                                          tuple_,
                                          dict_,)]
    print(types)

if __name__ == '__main__':
    data_types()