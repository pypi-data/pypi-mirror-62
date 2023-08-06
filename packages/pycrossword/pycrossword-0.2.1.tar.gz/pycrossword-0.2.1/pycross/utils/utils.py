# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Iskander Shafikov <s00mbre@gmail.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

## @package utils.utils
import sys, os, subprocess, traceback, uuid, tempfile, platform, re, json
from datetime import datetime, time

from .globalvars import *
from PyQt5 import QtGui, QtCore, QtWidgets

# ---------------------------- COMMON ---------------------------- #

def is_iterable(obj):
    if isinstance(obj, str): return False
    try:
        _ = iter(obj)
        return True
    except:
        return False

def getosname():
    return platform.system()

def generate_uuid():
    return uuid.uuid4().hex

def walk_dir(root_path, abs_path=True, recurse=True, dir_process_function=None,
             file_process_function=None, file_types=None):
    """
    """
    if abs_path:
        root_path = os.path.abspath(root_path)
    for (d, dirs, files) in os.walk(root_path):
        if dir_process_function:
            for d_ in dirs:
                dir_process_function(os.path.join(d, d_))
        if file_process_function:
            for f in files:
                ext = os.path.splitext(f)[1][1:].lower()
                if (not file_types) or (ext in file_types):
                    file_process_function(os.path.join(d, f))
        if not recurse: break

def run_exe(args, external=False, capture_output=True, stdout=subprocess.PIPE, encoding=ENCODING,
            timeout=None, shell=False, **kwargs):
    try:
        osname = platform.system()
        if external:
            if osname == 'Windows':
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
                return subprocess.Popen(args,
                    creationflags=creationflags,
                    stdout=stdout if capture_output else None,
                    stderr=subprocess.STDOUT if capture_output else None,
                    encoding=encoding, shell=shell, **kwargs)
            else:
                return subprocess.Popen('nohup ' + (args if isinstance(args, str) else ' '.join(args)),
                    stdout=stdout if capture_output else None,
                    stderr=subprocess.STDOUT if capture_output else None,
                    encoding=encoding, shell=shell, preexec_fn=os.setpgrp,
                    **kwargs)
        else:
            return subprocess.run(args,
                capture_output=capture_output,
                encoding=encoding,
                timeout=timeout, shell=shell, **kwargs)
    except Exception as err:
        traceback.print_exc(limit=None)
        raise

def datetime_to_str(dt=None, strformat='%Y-%m-%d %H-%M-%S'):
    if dt is None: dt = datetime.now()
    return dt.strftime(strformat)

def timestamp_to_str(ts=None, strformat='%Y-%m-%d %H-%M-%S'):
    if ts is None: ts = time.time()
    return datetime_to_str(datetime.fromtimestamp(ts), strformat)

def str_to_datetime(text, strformat='%Y-%m-%d %H-%M-%S'):
    return datetime.strptime(text, strformat)

def str_to_timestamp(text, strformat='%Y-%m-%d %H-%M-%S'):
    return str_to_datetime(text, strformat).timestamp()

def get_tempdir():
    return os.path.abspath(tempfile.gettempdir())

def bytes_human(value, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(value) < 1024.0:
            return f"{value:3.1f}{unit}{suffix}"
        value /= 1024.0
    return f"{value:.1f}Yi{suffix}"

def restart_app(closefunction):
    osname = platform.system()
    run_exe('pythonw cwordg.py' if osname == 'Windows' else 'python3 ./cwordg.py', external=True, capture_output=False, shell=True)
    closefunction()

def file_types_registered(filetypes=('xpf', 'ipuz', 'pxjson')):
    osname = platform.system()
    if osname == 'Windows':
        import winreg
        try:
            root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            hKey = winreg.OpenKeyEx(root, f"Software\\Classes\\{APP_NAME}\\shell\\open\\command")
            if winreg.QueryValue(hKey, '') != f'"{make_abspath(sys.executable)}" "{make_abspath(sys.argv[0])}" -o "%1"':
                winreg.CloseKey(hKey)
                return False
            winreg.CloseKey(hKey)
            for filetype in filetypes:
                ftype = ('.' + filetype.lower()) if not filetype.startswith('.') else filetype.lower()
                hKey = winreg.OpenKeyEx(root, f"Software\\Classes\\{ftype}")
                if winreg.QueryValue(hKey, '') != APP_NAME:
                    winreg.CloseKey(hKey)
                    return False
                winreg.CloseKey(hKey)
            return True
        except:
            return False

    elif osname == 'Linux':
        appname = APP_NAME.lower()
        res = run_exe(f'xdg-mime query default x-scheme-handler/{appname}', False, True, shell=True)
        return os.path.isfile(os.path.expanduser(LINUX_APP_PATH)) and \
                os.path.isfile(os.path.expanduser(LINUX_MIME_XML)) and \
                res.returncode == 0 and \
                res.stdout.strip() == f"{appname}.desktop"

    elif osname == 'Darwin':
        # see https://stackoverflow.com/a/2976711
        return False

    return False

def register_file_types(filetypes=('xpf', 'ipuz', 'pxjson'), register=True):
    if not filetypes: return False
    osname = platform.system()
    if osname == 'Windows':
        import winreg
        try:
            root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            # app entry
            if register:
                hKey = winreg.CreateKey(root, f"Software\\Classes\\{APP_NAME}\\shell\\open\\command")
                winreg.SetValueEx(hKey, '', 0, winreg.REG_SZ, f'"{make_abspath(sys.executable)}" "{make_abspath(sys.argv[0])}" -o "%1"')
                winreg.CloseKey(hKey)
                hKey = winreg.CreateKey(root, f"Software\\Classes\\{APP_NAME}\\DefaultIcon")
                winreg.SetValueEx(hKey, '', 0, winreg.REG_SZ, f"{ICONFOLDER}\\main.ico")
                winreg.CloseKey(hKey)
            else:
                try:
                    hKey = winreg.OpenKeyEx(root, f"Software\\Classes\\{APP_NAME}", 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(hKey, 'DefaultIcon')
                except:
                    pass
                try:
                    hKey = winreg.OpenKeyEx(root, f"Software\\Classes\\{APP_NAME}\\shell\\open", 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(hKey, 'command')
                    hKey = winreg.OpenKeyEx(root, f"Software\\Classes\\{APP_NAME}\\shell", 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(hKey, 'open')
                    hKey = winreg.OpenKeyEx(root, f"Software\\Classes\\{APP_NAME}", 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(hKey, 'shell')
                    hKey = winreg.OpenKeyEx(root, f"Software\\Classes", 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(hKey, APP_NAME)
                except:
                    pass
            # ext entries
            for filetype in filetypes:
                ftype = ('.' + filetype.lower()) if not filetype.startswith('.') else filetype.lower()
                if register:
                    hKey = winreg.CreateKey(root, f"Software\\Classes\\{ftype}")
                    winreg.SetValueEx(hKey, '', 0, winreg.REG_SZ, APP_NAME)
                    winreg.CloseKey(hKey)
                else:
                    try:
                        hKey = winreg.OpenKeyEx(root, f"Software\\Classes", 0, winreg.KEY_ALL_ACCESS)
                        winreg.DeleteKey(hKey, ftype)
                    except:
                        continue

            winreg.CloseKey(root)

            # fast update file icons
            run_exe('ie4uinit.exe -show', False, False, shell=True)
            return True

        except Exception as err:
            print(str(err))
            return False

    elif osname == 'Linux':
        # example at https://askubuntu.com/questions/108925/how-to-tell-chrome-what-to-do-with-a-magnet-link/133693#133693
        appname = APP_NAME.lower()
        if register:
            # create MIME app in '~/.local/share/applications'
            with open(os.path.expanduser(LINUX_APP_PATH), 'w') as f:
                f.write(LINUX_MIME_APP.format(f'python3 "{make_abspath(sys.argv[0])}" -o',
                        appname, f"{APP_NAME} launcher"))
            # add row to '~/.local/share/applications/mimeapps.list'
            res = run_exe(f"xdg-mime default {appname}.desktop x-scheme-handler/{appname}", shell=True)
            if res.returncode: return False
            # check successful assignment
            res = run_exe(f'xdg-mime query default x-scheme-handler/{appname}', shell=True)
            if res.returncode or res.stdout.strip() != f"{appname}.desktop":
                # failed to add association
                return False
            # install MIME types
            ftypes = []
            for filetype in filetypes:
                ftype = ('.' + filetype.lower()) if not filetype.startswith('.') else filetype.lower()
                ftypes.append(f'<glob pattern="*{ftype}"/>')
            with open(os.path.expanduser(LINUX_MIME_XML), 'w') as f:
                f.write(LINUX_MIME_TYPES.format(f"x-scheme-handler/{appname}",
                        f"{APP_NAME} settings and cw files", '\n    '.join(ftypes)))
            res = run_exe(f'xdg-mime install {LINUX_MIME_XML}', shell=True)
            if res.returncode: return False
            # install icon
            res = run_exe(f'xdg-icon-resource install --context mimetypes --size 64 {ICONFOLDER}/main.png x-scheme-handler-{appname}', shell=True)
            return not res.returncode and not res.stdout.strip()

        else:
            try:
                # uninstall icon
                run_exe(f'xdg-icon-resource uninstall --size 64 {ICONFOLDER}/main', capture_output=False, shell=True)
                # uninstall MIME types
                run_exe(f'xdg-mime uninstall {LINUX_MIME_XML}', capture_output=False, shell=True)
                # delete MIME XML
                run_exe(f'rm {LINUX_MIME_XML}', capture_output=False, shell=True)
                # delete MIME app
                run_exe(f'rm {LINUX_APP_PATH}', capture_output=False, shell=True)
                return True
            except:
                return False

    elif osname == 'Darwin':
        # see https://stackoverflow.com/a/2976711
        return False

    # some oddball os...
    return False

# ---------------------------- GUI ---------------------------- #

class QThreadStump(QtCore.QThread):

    sig_error = QtCore.pyqtSignal(QtCore.QThread, str)

    def __init__(self, default_priority=QtCore.QThread.NormalPriority,
                 on_start=None, on_finish=None, on_run=None, on_error=None,
                 start_signal=None, stop_signal=None,
                 free_on_finish=False, start_now=False, can_terminate=True):
        super().__init__()
        self.init(default_priority, on_start, on_finish, on_run, on_error,
                  start_signal, stop_signal, free_on_finish, can_terminate)
        if start_now: self.start()

    def __del__(self):
        try:
            self.wait()
        except:
            pass

    def init(self, default_priority=QtCore.QThread.NormalPriority,
             on_start=None, on_finish=None, on_run=None, on_error=None,
             start_signal=None, stop_signal=None,
             free_on_finish=False, can_terminate=True):
        try:
            self.started.disconnect()
            self.finished.disconnect()
            self.sig_error.disconnect()
        except:
            pass

        self.setTerminationEnabled(can_terminate)
        if on_start: self.started.connect(on_start)
        if on_finish: self.finished.connect(on_finish)
        if free_on_finish: self.finished.connect(self.deleteLater)
        if start_signal: start_signal.connect(self.start)
        if stop_signal: stop_signal.connect(self.terminate)
        if on_error: self.sig_error.connect(on_error)
        self.default_priority = default_priority if default_priority != QtCore.QThread.InheritPriority else QtCore.QThread.NormalPriority
        self.on_run = on_run
        self.mutex = QtCore.QMutex()

    def lock(self):
        self.mutex.lock()

    def unlock(self):
        self.mutex.unlock()

    def run(self):
        self.setPriority(self.default_priority)
        if self.on_run and not self.isInterruptionRequested():
            try:
                self.on_run()
            except Exception as err:
                traceback.print_exc(limit=None)
                self.sig_error.emit(self, str(err))

# ------------------------------------------------------------------------ #

def make_font(family, size=-1, weight=-1, italic=False, font_unit='pt'):
    font = QtGui.QFont(family)
    if font_unit == 'pt':
        font.setPointSize(size)
    else:
        font.setPixelSize(size)
    font.setWeight(weight)
    font.setItalic(italic)
    #print(f"make_font: font_unit={font_unit}, family={font.family()}, size(pt) = {font.pointSize()}, size(px)={font.pixelSize()}")
    return font

MSGBOX_BUTTONS = {'ok': (_('OK'), QtWidgets.QMessageBox.AcceptRole), 'yes': (_('Yes'), QtWidgets.QMessageBox.YesRole),
                  'no': (_('No'), QtWidgets.QMessageBox.NoRole), 'cancel': (_('Cancel'), QtWidgets.QMessageBox.RejectRole),
                  'yesall': (_('Yes to All'), QtWidgets.QMessageBox.YesRole), 'noall': (_('No to All'), QtWidgets.QMessageBox.NoRole),
                  'apply': (_('Apply'), QtWidgets.QMessageBox.ApplyRole), 'reset': (_('Reset'), QtWidgets.QMessageBox.ResetRole),
                  'open': (_('Open'), QtWidgets.QMessageBox.AcceptRole), 'save': (_('Save'), QtWidgets.QMessageBox.AcceptRole),
                  'close': (_('Close'), QtWidgets.QMessageBox.RejectRole), 'discard': (_('Discard'), QtWidgets.QMessageBox.DestructiveRole),
                  'restoredefaults': (_('Restore Defaults'), QtWidgets.QMessageBox.ResetRole), 'help': (_('Help'), QtWidgets.QMessageBox.HelpRole),
                  'saveall': (_('Save All'), QtWidgets.QMessageBox.AcceptRole), 'abort': (_('Abort'), QtWidgets.QMessageBox.RejectRole),
                  'retry': (_('Retry'), QtWidgets.QMessageBox.AcceptRole), 'ignore': (_('Ignore'), QtWidgets.QMessageBox.AcceptRole)}
MSGBOX_TYPES = {'error': (QtWidgets.QMessageBox.Critical, ['ok']), 'warn': (QtWidgets.QMessageBox.Warning, ['ok']), 'ask': (QtWidgets.QMessageBox.Question, ['yes', 'no']),
                'info': (QtWidgets.QMessageBox.Information, ['ok']), '-': (QtWidgets.QMessageBox.NoIcon, ['ok'])}

def MsgBox(what, parent=None, title='pyCross', msgtype='info', btn=None, detailedText='', infoText='', execnow=True):
    msgtype = MSGBOX_TYPES.get(msgtype, MSGBOX_TYPES['-'])
    msgbox = QtWidgets.QMessageBox(parent)
    msgbox.setIcon(msgtype[0])
    msgbox.setWindowTitle(title)
    msgbox.setText(what)
    msgbox.setDetailedText(detailedText)
    msgbox.setInformativeText(infoText)
    if not btn: btn = msgtype[1]
    for bt in btn:
        if bt in MSGBOX_BUTTONS:
            msgbox.addButton(MSGBOX_BUTTONS[bt][0], MSGBOX_BUTTONS[bt][1])
    if execnow:
        msgbox.exec()
        clk = msgbox.clickedButton()
        if not clk: return ''
        clktxt = clk.text()
        for bt in MSGBOX_BUTTONS:
            if MSGBOX_BUTTONS[bt][0] == clktxt:
                return bt
        return ''
    else:
        return msgbox

def UserInput(dialogtype='text', parent=None, title='pyCross', label='', value=None, textmode='normal',
              valrange=None, decimals=1, step=1, comboeditable=True, comboitems=[]):
    modes = {'normal': QtWidgets.QLineEdit.Normal, 'noecho': QtWidgets.QLineEdit.NoEcho,
             'password': QtWidgets.QLineEdit.Password, 'passwordonedit': QtWidgets.QLineEdit.PasswordEchoOnEdit}
    if dialogtype == 'text':
        mode = modes[textmode]
        return QtWidgets.QInputDialog.getText(parent, title, label,
                echo=mode, text=str(value) if value else '')
    elif dialogtype == 'multitext':
        return QtWidgets.QInputDialog.getMultiLineText(parent, title, label,
                text=str(value) if value else '')
    elif dialogtype == 'int':
        return QtWidgets.QInputDialog.getInt(parent, title, label,
                value=int(value) if value else 0, min=valrange[0] if valrange else -2147483647,
                max=valrange[1] if valrange else 2147483647, step=step)
    elif dialogtype == 'float':
        return QtWidgets.QInputDialog.getDouble(parent, title, label,
                value=float(value) if value else 0, min=valrange[0] if valrange else -2147483647,
                max=valrange[1] if valrange else 2147483647, decimals=decimals)
    elif dialogtype == 'item':
        return QtWidgets.QInputDialog.getMultiLineText(parent, title, label,
                comboitems, current=value if value else 0, editable=comboeditable)

def clipboard_copy(value, valtype='text'):
    clip = QtWidgets.qApp.clipboard()
    if valtype == 'text':
        clip.setText(value)
    elif valtype == 'mime':
        clip.setMimeData(value)
    elif valtype == 'pixmap':
        clip.setPixmap(value)
    elif valtype == 'image':
        clip.setImage(value)

def clipboard_get(valtype='text'):
    clip = QtWidgets.qApp.clipboard()
    if valtype == 'text':
        return clip.text()
    elif valtype == 'mime':
        return clip.mimeData()
    elif valtype == 'pixmap':
        return clip.pixmap()
    elif valtype == 'image':
        return clip.image()
    return None

def clipboard_clear():
    QtWidgets.qApp.clipboard().clear()

def stylesheet_load(style, dequote=True, strip_sz=True, units=('pt', 'px')):
    ls_style = [s.strip() for s in style.split(';')]
    d = {}
    def unq(s):
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        return s
    for pair in ls_style:
        st = [s.strip() for s in pair.split(':')]
        if len(st) != 2: continue
        if dequote: st[1] = unq(st[1])
        if strip_sz:
            for unit in units:
                if st[1].endswith(unit):
                    st[1] = int(st[1][:-2].strip())
                    break
        if st[1] == 'true': st[1] = True
        if st[1] == 'false': st[1] = False
        d[st[0]] = st[1]
    #print(f"_stylesheet_load: {d}")
    return d

def stylesheet_dump(d, quoted_keys=('font-family',), add_units={'font-size': 'pt', 'border': 'px', 'border-width': 'px'}):
    l = []
    for key in d:
        val = d[key]
        for qk in quoted_keys:
            if key == qk and not (val.startswith('"') and val.endswith('"')):
                val = f'"{val}"'
                break
        unit = add_units.get(key, '')
        if unit: val = f'{val}{unit}'
        if isinstance(val, bool): val = str(val).lower()
        l.append(f'{key}: {str(val)}')
    s = '; '.join(l)
    #print(f"_stylesheet_dump: {s}")
    return s

def font_weight_css2qt(weight, default=0):
    if weight == 'normal':
        weight = QtGui.QFont.Normal
    elif weight == 'bold':
        weight = QtGui.QFont.Bold
    else:
        weight = FONT_WEIGHTS.get(int(weight), default)
    return weight

def font_weight_qt2css(weight, default=0):
    for w in FONT_WEIGHTS:
        if FONT_WEIGHTS[w] == weight:
            return w
    return default

def font_from_stylesheet(style, font_unit='pt', default_font=None):
    dic_style = stylesheet_load(style)
    if not 'font-family' in dic_style:
        if not default_font:
            return None
        else:
            dic_style['font-family'] = default_font.family()
    if not 'font-size' in dic_style:
        if not default_font:
            return None
        else:
            dic_style['font-size'] = default_font.pointSize() if font_unit == 'pt' else default_font.pixelSize()
    if not 'font-weight' in dic_style:
        if not default_font:
            return None
        else:
            dic_style['font-weight'] = font_weight_qt2css(default_font.weight())
    if not 'font-style' in dic_style:
        dic_style['font-style'] = 'normal'

    font =  make_font(dic_style['font-family'], dic_style['font-size'], font_weight_css2qt(dic_style['font-weight']), (dic_style['font-style'] == 'italic'), font_unit)
    #print(f"FONT: font_unit={font_unit}, family={font.family()}, size(pt)={font.pointSize()}, size(px)={font.pixelSize()}, weight={font.weight()}")
    return font

def font_to_stylesheet(font, style, font_unit='pt'):
    dic_style = stylesheet_load(style)
    dic_style['font-family'] = font.family()
    dic_style['font-size'] = font.pointSize() if font_unit == 'pt' else font.pixelSize()
    dic_style['font-weight'] = font_weight_qt2css(font.weight())
    dic_style['font-style'] = 'italic' if font.italic() else 'normal'
    return stylesheet_dump(dic_style, add_units={'font-size': font_unit})

def color_from_stylesheet(style, tag='background-color', default='black'):
    dic_style = stylesheet_load(style)
    return QtGui.QColor(dic_style.get(tag, default))

def color_to_stylesheet(color, style, tag='background-color'):
    dic_style = stylesheet_load(style)
    dic_style[tag] = color.name(1)
    return stylesheet_dump(dic_style)

def property_to_stylesheet(propname, propvalue, style):
    dic_style = stylesheet_load(style)
    dic_style[propname] = propvalue
    return stylesheet_dump(dic_style)

def property_from_stylesheet(propname, style, default=None):
    dic_style = stylesheet_load(style)
    return dic_style.get(propname, default)

# ------------------------------------------------------------------------ #

## @brief Syntax highlighter class for JSON.
# Used in pycross::forms::WordSrcDialog (DB table definition).
# @see [QSyntaxHighlighter docs](https://doc.qt.io/qt-5/qsyntaxhighlighter.html)
class JsonHiliter(QtGui.QSyntaxHighlighter):

    ## @brief Regex-based patterns and their corresponding color values.
    # Each record has 3 elements:
    #   1. `Python regex object` compiled regex pattern
    #   2. `int` group number in regex match results to highlight 
    #   (0 = whole match, 1 = first expression in parentheses, etc...)
    #   3. `QtGui.QColor` color to apply to matched text
    PATTERNS = [
        # operators (dot, comma, colon)
        (re.compile(r'([\.,\:])'), 1, QtGui.QColor(QtCore.Qt.red)),
        # brackets
        (re.compile(r'([\{\}\[\]\(\)])'), 1, QtGui.QColor(QtCore.Qt.gray)),
        # numbers
        (re.compile(r'([\s,\:\{\[\(])([\-\+]?[\d\.]+)([\s,\:\}\]\)]?)'), 2, QtGui.QColor(QtCore.Qt.blue)),
        (re.compile(r'([\s,\:\{\[\(])([\-\+]?[\d\.]+$)'), 2, QtGui.QColor(QtCore.Qt.blue)),
        (re.compile(r'(^[\-\+]?[\d\.]+)([\s,\:\}\]\)]?)'), 1, QtGui.QColor(QtCore.Qt.blue)),
        (re.compile(r'(^[\-\+]?[\d\.]+$)'), 1, QtGui.QColor(QtCore.Qt.blue)),
        # boolean
        (re.compile(r'([\s,\:\{\[\(])(true|false)([\s,\:\}\]\)])'), 2, QtGui.QColor(QtCore.Qt.magenta)),
        (re.compile(r'([\s,\:\{\[\(])(true$|false$)'), 2, QtGui.QColor(QtCore.Qt.magenta)),
        (re.compile(r'(^true|^false)([\s,\:\}\]\)])'), 1, QtGui.QColor(QtCore.Qt.magenta)),
        (re.compile(r'(^true$|^false$)'), 1, QtGui.QColor(QtCore.Qt.magenta)),
        # null values
        (re.compile(r'([\s,\:\{\[\(])(null)([\s,\:\}\]\)])'), 2, QtGui.QColor(QtCore.Qt.gray)),
        (re.compile(r'([\s,\:\{\[\(])(null$)'), 2, QtGui.QColor(QtCore.Qt.gray)),
        (re.compile(r'(^null)([\s,\:\}\]\)])'), 1, QtGui.QColor(QtCore.Qt.gray)),
        (re.compile(r'(^null$)'), 1, QtGui.QColor(QtCore.Qt.gray)),
        # string values
        (re.compile(r'([\s,\:\[\(])(\".*?\")'), 2, QtGui.QColor(QtCore.Qt.darkCyan)),
        (re.compile(r'(^\".*?\")'), 1, QtGui.QColor(QtCore.Qt.darkCyan)),
        # key names
        (re.compile(r'(\".*?\")(\s*\:)'), 1, QtGui.QColor(QtCore.Qt.darkGreen))        
    ]

    sig_parse_error = QtCore.pyqtSignal(QtGui.QSyntaxHighlighter, str, str, int, int, int)
    sig_parse_success = QtCore.pyqtSignal(QtGui.QSyntaxHighlighter)

    def __init__(self, parent: QtGui.QTextDocument, decode_errors=False, 
        on_decode_error=None, on_decode_success=None):
        super().__init__(parent)
        ## `bool` whether JSON decode errors must be highlighted dynamically
        self.decode_errors = decode_errors
        if on_decode_error: self.sig_parse_error.connect(on_decode_error)
        if on_decode_success: self.sig_parse_success.connect(on_decode_success)
        self._error_format = QtGui.QTextCharFormat()
        self._error_format.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
        self._error_format.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.yellow)))
        self.decoder = json.JSONDecoder()

    def highlightBlock(self, text):
        # clear format
        length = self.currentBlock().length()
        #self.setFormat(0, length, QtGui.QTextCharFormat())
        # syntax highlighting
        for pattern in JsonHiliter.PATTERNS:
            gr = pattern[1]
            for m in pattern[0].finditer(text):
                try:
                    self.setFormat(m.start(gr), m.end(gr) - m.start(gr), pattern[2])
                except:
                    pass
        # error highlighting
        if not self.decode_errors: return
        doc = self.document()
        offset = self.currentBlock().position()        
        try:
            self.decoder.decode(doc.toPlainText())            
        except json.JSONDecodeError as err:
            if err.pos >= offset and err.pos < (offset + length):
                self.setFormat(err.pos - offset, 1, self._error_format)
            self.sig_parse_error.emit(self, err.msg, err.doc, err.pos, err.lineno, err.colno)
        else:
            self.sig_parse_success.emit(self)
