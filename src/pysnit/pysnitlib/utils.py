import importlib.util as imputl
import sys
import importlib


def load_module_from_path(module_name: str, module_path: str):
    """モジュールの名前とファイルパスからモジュールを動的にimportする
    :param module_name: 読み込むモジュールに付与する名前
    :param module_path: モジュールのファイルパス
    :return module: import済みモジュール
    """
    spec = imputl.spec_from_file_location(module_name, module_path)
    module = imputl.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def remove_decorator(srccode: str, decorator: str) -> str:
    """getsourceの返り値からデコレータ部分を取り除く
    :param srccode: getsourceの返り値
    :param decorator: 取り除きたいデコレータ ex: '@snippet'
    :return srccode_without_decorator: デコレータを取り除いたもの
    """
    stack = []
    len_deco = len(decorator)

    # no snippet mark remained
    if srccode.find('@snippet') != 0:
        return srccode.strip()

    # no option
    if srccode[len_deco] != '(':
        return srccode[len_deco:].strip()

    stack.append('(')
    i = len_deco + 1
    while stack:
        top = stack[-1]
        nchr = srccode[i]
        if top == '(':
            if nchr == ')':
                stack.pop()
            elif nchr == "'" or nchr == '"':
                stack.append(nchr)
        elif top == "'":
            if nchr == "'":
                stack.pop()
        elif top == '"':
            if nchr == '"':
                stack.pop()
        i += 1

    return srccode[i:].strip()
