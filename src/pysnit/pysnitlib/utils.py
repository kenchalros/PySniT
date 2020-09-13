import importlib.util as imputl
import sys
import importlib

def load_module_from_path(module_name, module_path):
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