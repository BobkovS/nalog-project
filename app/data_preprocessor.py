def inn_json_is_correct(json):
    if not all(name in json for name in ['fam', 'nam', 'otch', 'bdate', 'bplace', 'docno', 'docdt']):
        return False
    return True


def suspension_json_is_correct(json):
    if not all(name in json for name in ['inn', 'bikPRS']):
        return False
    return True


def prepare_inn_json(json):
    data = {"fam": json['fam'], "nam": json['nam'], "bdate": json['bdate'], "bplace": json['bplace'], "doctype": "21",
            "docno": json['docno'], "docdt": json['docdt'], "captcha": "", "captchaToken": "", "c": "innMy"}
    data.update({"otch": json['otch']}) if json['otch'] else data.update({"opt_otch": 1})
    return data


def prepare_suspension_json(json):
    return {'requestType': 'FINDPRS', 'innPRS': json['inn'], 'bikPRS': json['bikPRS'], 'fileName': '', 'fileNameED': '',
            'bik': '', 'kodTU': '', 'dateSAFN': '', 'bikAFN': '', 'dateAFN': '', 'captcha': '', 'captchaToken': ''}
