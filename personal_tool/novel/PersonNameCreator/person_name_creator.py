from person_name_creator.feature.surname.surname_feature import SurnameFeature


class PersonNameCreator:
    """人名生成器"""

    def main(self, surname: str = None):
        # 获取姓氏
        surname = SurnameFeature.get_surname(surname)
        print(surname)


if __name__ == '__main__':
    person_name_creator = PersonNameCreator()
    person_name_creator.main()
