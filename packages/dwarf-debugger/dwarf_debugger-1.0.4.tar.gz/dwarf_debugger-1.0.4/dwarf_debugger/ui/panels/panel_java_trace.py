"""
Dwarf - Copyright (C) 2019 Giovanni Rocca (iGio90)
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
import json
from math import ceil, floor
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QPainter, QColor, QTextOption, QFontMetrics, QFont, QPolygon, QIcon, QStandardItemModel, \
    QStandardItem
from PyQt5.QtWidgets import QSplitter, QListWidget, QScrollBar, QMenu, QWidget, QVBoxLayout, QAbstractScrollArea, QToolBar, QLabel, \
    QSizePolicy

from dwarf_debugger.ui.dialogs.dialog_input import InputDialog
from dwarf_debugger.ui.widgets.list_view import DwarfListView

from dwarf_debugger.lib import utils

# a list of classes you generally want to trace
PREFIXED_CLASS = [
    'android.util.Base64',
    'java.security.MessageDigest',
    'java.util.zip.GZIPOutputStream'
]


class JavaTraceView(QAbstractScrollArea):

    def __init__(self, parent=None):
        super(JavaTraceView, self).__init__(parent=parent)

        self.data = []
        self.search_result = []

        # setting font
        self.font = utils.get_os_monospace_font()
        self.font.setFixedPitch(True)
        self.setFont(self.font)

        self._char_width = self.fontMetrics().width("2")
        self._char_height = self.fontMetrics().height()
        self._base_line = self.fontMetrics().ascent()
        self._has_scrolled = False

        self._data_height = 0

        self.verticalScrollBar().rangeChanged.connect(self._scroll_bottom)
        self.verticalScrollBar().valueChanged.connect(self._check_scroll)

    def add_event(self, data):
        self.data.append(data)
        maximum = len(self.data) - self.visible_lines() + 1
        if self._data_height > maximum:
            maximum = int(ceil(self._data_height / self._char_height))
        self.verticalScrollBar().setRange(0, maximum)
        self.verticalScrollBar().setPageStep(self.visible_lines())

    def _scroll_bottom(self, scroll_min, scroll_max):
        if not self._has_scrolled:
            self.verticalScrollBar().setValue(scroll_max)

    def _check_scroll(self, value):
        if value < self.verticalScrollBar().maximum():
            # user scrolled so stop autoscroll
            self._has_scrolled = True
        elif value == self.verticalScrollBar().maximum():
            # scrolled back to bottom so do autoscroll again
            self._has_scrolled = False

    def visible_lines(self):
        """ returns number of lines that fits viewport
        """
        height = self.viewport().height()
        num_lines = int(ceil(height / self._char_height))
        return num_lines + 1

    # def adjust(self):
    #    for x in self.data:

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.fillRect(0, 0, self.viewport().width(), self.viewport().height(), QColor('#181818'))

        self.pos = self.verticalScrollBar().value()
        data_start = 0
        data_end = 0

        if len(self.data) > self.visible_lines():
            data_start = self.pos
            data_end = self.pos + self.visible_lines()
        else:
            data_end = len(self.data)

        drawing_pos_y = 10
        trace_depth = 0

        fontMetrics = QFontMetrics(QFont(self.font))
        text_options = QTextOption()
        text_options.setAlignment(Qt.AlignLeft)
        text_options.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        for i, line in enumerate(self.data):
            if i == self.pos:
                break
            if line['event'] == 'leave':
                trace_depth -= 1
            elif line['event'] == 'enter':
                trace_depth += 1

        for i, line in enumerate(self.data[data_start:data_end]):
            if i > self.visible_lines():
                break

            is_obj = False
            if isinstance(line['data'], str) and line['data'].startswith('{'):
                is_obj = True
                line['data'] = json.loads(line['data'])

            drawing_pos_x = 10
            painter.setPen(QColor('#fff'))

            if line['event'] == 'leave':
                if trace_depth:
                    trace_depth -= 1
                drawing_pos_x += (trace_depth * 20)
                painter.setPen(QColor('crimson'))
                painter.setBrush(QColor('#222'))
                polygon = QPolygon()
                polygon.append(QPoint(drawing_pos_x - 6, drawing_pos_y + (self._char_height * 0.5)))
                polygon.append(QPoint(drawing_pos_x + 10, drawing_pos_y - (self._char_height * 0.5)))
                polygon.append(QPoint(self.viewport().width() - 21, drawing_pos_y - (self._char_height * 0.5)))
                polygon.append(QPoint(self.viewport().width() - 21, drawing_pos_y + self._char_height + (self._char_height * 0.5)))
                polygon.append(QPoint(drawing_pos_x + 10, drawing_pos_y + self._char_height + (self._char_height * 0.5)))
                polygon.append(QPoint(drawing_pos_x - 6, drawing_pos_y + (self._char_height * 0.5)))
                painter.drawPolygon(polygon)
            elif line['event'] == 'enter':
                trace_depth += 1
                drawing_pos_x += (trace_depth * 20)
                painter.setPen(QColor('yellowgreen'))
                painter.setBrush(QColor('#222'))
                polygon = QPolygon()
                polygon.append(QPoint(drawing_pos_x + 6, drawing_pos_y - (self._char_height * 0.5)))
                polygon.append(QPoint(int(floor(self.viewport().width())) - 21, drawing_pos_y - (self._char_height * 0.5)))
                polygon.append(QPoint(int(floor(self.viewport().width())) - 5, drawing_pos_y + (self._char_height * 0.5)))
                polygon.append(QPoint(int(floor(self.viewport().width())) - 21, drawing_pos_y + self._char_height + (self._char_height * 0.5)))
                polygon.append(QPoint(drawing_pos_x + 6, drawing_pos_y + self._char_height + (self._char_height * 0.5)))
                #polygon.append(QPoint(drawing_pos_x + 21, drawing_pos_y + (self._char_height * 0.5)))
                polygon.append(QPoint(drawing_pos_x + 6, drawing_pos_y - (self._char_height * 0.5)))
                painter.drawPolygon(polygon)

            drawing_pos_x += 20
            rect = QRectF(drawing_pos_x, drawing_pos_y, self.viewport().width() - 25 - drawing_pos_x, self._char_height + 10)

            if line['event'] == 'enter':
                arg_str = '('
                for a in range(len(line['data'])):
                    arg_str += 'arg_{0}, '.format(a)

                if len(line['data']):
                    arg_str = arg_str[:-2]
                arg_str += ')'
                painter.drawText(rect, line['class'] + arg_str, option=text_options)
            else:
                painter.drawText(rect, line['class'], option=text_options)

            drawing_pos_y += self._char_height + 15

            if isinstance(line['data'], str):
                if line['data']:
                    rect = fontMetrics.boundingRect(drawing_pos_x, drawing_pos_y, self.viewport().width() - drawing_pos_x - 25, 0, Qt.AlignLeft | Qt.TextWordWrap | Qt.TextWrapAnywhere, line['data'])
                    rect = QRectF(drawing_pos_x, drawing_pos_y, rect.width(), rect.height())
                    painter.setPen(QColor('#888'))
                    painter.drawText(rect, line['data'], option=text_options)
                    drawing_pos_y += rect.height() + 5
            else:
                width = int(floor(self.viewport().width() - drawing_pos_x - (5 * self._char_width) - 35))
                max_chars = int(floor(width / self._char_width))
                hold_x = drawing_pos_x + 5
                width -= 20
                painter.setPen(QColor('#888'))
                for data in line['data']:
                    drawing_pos_x = hold_x
                    if isinstance(line['data'][data], int):
                        text = '{0:d}'.format(line['data'][data])
                    elif isinstance(line['data'][data], str):
                        text = line['data'][data]
                    elif isinstance(line['data'][data], list):
                        text = str(line['data'][data])
                    else:
                        text = str(line['data'][data])

                    if line['event'] == 'enter':
                        arg = 'arg_{0}: '.format(data)
                        painter.drawText(drawing_pos_x, drawing_pos_y + self._base_line, arg)
                        drawing_pos_x += len(arg) * self._char_width
                    elif line['event'] == 'leave':
                        retval = data + ': '
                        painter.drawText(drawing_pos_x, drawing_pos_y + self._base_line, retval)
                        drawing_pos_x += len(retval) * self._char_width

                    if len(text) * self._char_width < width:
                        painter.drawText(drawing_pos_x, drawing_pos_y + self._base_line, text)
                        drawing_pos_y += self._char_height + 5
                    else:
                        rect = fontMetrics.boundingRect(drawing_pos_x, drawing_pos_y, width, 0, Qt.AlignLeft | Qt.TextWordWrap | Qt.TextWrapAnywhere, text)
                        rect = QRectF(rect)
                        painter.drawText(rect, text, option=text_options)
                        drawing_pos_y += rect.height() + 5

            drawing_pos_y += self._char_height + 5
            #self._data_height += drawing_pos_y

    def clear(self):
        self.data = []


class JavaTracePanel(QWidget):
    def __init__(self, app, *__args):
        super().__init__(app)
        self.app = app

        self.app.dwarf.onJavaTraceEvent.connect(self.on_event)
        self.app.dwarf.onEnumerateJavaClassesStart.connect(self.on_enumeration_start)
        self.app.dwarf.onEnumerateJavaClassesMatch.connect(self.on_enumeration_match)
        self.app.dwarf.onEnumerateJavaClassesComplete.connect(self.on_enumeration_complete)

        self.tracing = False
        self.trace_classes = []
        self.trace_depth = 0

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self._record_icon = QIcon(utils.resource_path('assets/icons/record.png'))
        self._pause_icon = QIcon(utils.resource_path('assets/icons/pause.png'))
        self._stop_icon = QIcon(utils.resource_path('assets/icons/stop.png'))

        self._tool_bar = QToolBar()
        self._tool_bar.addAction('Start', self.start_trace)
        self._tool_bar.addAction('Pause', self.pause_trace)
        self._tool_bar.addAction('Stop', self.stop_trace)
        self._tool_bar.addSeparator()
        self._entries_lbl = QLabel('Entries: 0')
        self._entries_lbl.setStyleSheet('color: #ef5350;')
        self._entries_lbl.setContentsMargins(10, 0, 10, 2)
        self._entries_lbl.setAttribute(Qt.WA_TranslucentBackground, True) # keep this
        self._entries_lbl.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self._entries_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._tool_bar.addWidget(self._entries_lbl)

        layout.addWidget(self._tool_bar)

        self.setup_splitter = QSplitter()
        self.events_list = JavaTraceView(self)
        self.events_list.setVisible(False)

        self.trace_list = DwarfListView()
        self.trace_list_model = QStandardItemModel(0, 1)
        self.trace_list_model.setHeaderData(0, Qt.Horizontal, 'Traced')
        self.trace_list.setModel(self.trace_list_model)

        self.trace_list.doubleClicked.connect(self.trace_list_double_click)

        self.class_list = DwarfListView()
        self.class_list_model = QStandardItemModel(0, 1)
        self.class_list_model.setHeaderData(0, Qt.Horizontal, 'Classes')
        self.class_list.setModel(self.class_list_model)

        self.class_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.class_list.customContextMenuRequested.connect(self.show_class_list_menu)
        self.class_list.doubleClicked.connect(self.class_list_double_click)

        self.current_class_search = ''

        bar = QScrollBar()
        bar.setFixedWidth(0)
        bar.setFixedHeight(0)
        self.trace_list.setHorizontalScrollBar(bar)
        bar = QScrollBar()
        bar.setFixedWidth(0)
        bar.setFixedHeight(0)
        self.class_list.setHorizontalScrollBar(bar)

        self.setup_splitter.addWidget(self.trace_list)
        self.setup_splitter.addWidget(self.class_list)

        layout.addWidget(self.setup_splitter)
        layout.addWidget(self.events_list)

        self.setLayout(layout)

    def class_list_double_click(self, item):
        item = self.class_list_model.itemFromIndex(item)
        try:
            if self.trace_classes.index(item.text()) >= 0:
                return
        except:
            pass
        self.trace_classes.append(item.text())
        self.trace_list_model.appendRow([QStandardItem(item.text())])
        self.trace_list_model.sort(0, Qt.AscendingOrder)

    def on_enumeration_start(self):
        self.class_list_model.setRowCount(0)

    def on_enumeration_match(self, java_class):
        try:
            if PREFIXED_CLASS.index(java_class) >= 0:
                try:
                    if self.trace_classes.index(java_class) >= 0:
                        return
                except:
                    pass
                self.trace_list_model.appendRow(QStandardItem(java_class))
                self.trace_classes.append(java_class)
        except:
            pass

        self.class_list_model.appendRow([QStandardItem(java_class)])

    def on_enumeration_complete(self):
        self.class_list_model.sort(0, Qt.AscendingOrder)
        self.trace_list_model.sort(0, Qt.AscendingOrder)

    def on_event(self, data):
        trace, event, clazz, data = data
        if trace == 'java_trace':
            self.events_list.add_event(
                {
                    'event': event,
                    'class': clazz,
                    'data': data.replace(',', ', ')
                }
            )
            self._entries_lbl.setText('Events: %d' % len(self.events_list.data))

    def pause_trace(self):
        self.app.dwarf.dwarf_api('stopJavaTracer')
        self.tracing = False

    def show_class_list_menu(self, pos):
        menu = QMenu()
        search = menu.addAction('Search')
        action = menu.exec_(self.class_list.mapToGlobal(pos))
        if action:
            if action == search:
                self.class_list._on_cm_search()

    def start_trace(self):
        self.app.dwarf.dwarf_api('startJavaTracer', [self.trace_classes])
        self.trace_depth = 0
        self.tracing = True
        self.setup_splitter.setVisible(False)
        self.events_list.setVisible(True)

    def stop_trace(self):
        self.app.dwarf.dwarf_api('stopJavaTracer')
        self.tracing = False
        self.setup_splitter.setVisible(True)
        self.events_list.setVisible(False)
        self.events_list.clear()

    def trace_list_double_click(self, model_index):
        row = self.trace_list_model.itemFromIndex(model_index).row()
        if row != -1:
            trace_entry = self.trace_list_model.item(row, 0).text()

            if not trace_entry:
                return

            try:
                index = self.trace_classes.index(trace_entry)
                self.trace_classes.pop(index)
                self.trace_list_model.removeRow(row)
            except ValueError:
                pass


    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_F:
                self.search()
        super(JavaTracePanel, self).keyPressEvent(event)
