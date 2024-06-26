MAIN_STYLE = """/* /////////////////////////////////////////////////////////////////////////////////////////////////

SET APP STYLESHEET - FULL STYLES HERE
DARK THEME - DRACULA COLOR BASED

///////////////////////////////////////////////////////////////////////////////////////////////// */

QWidget{
    color: rgb(221, 221, 221);
    font: 10pt \ Segoe UI\ ;
}

/* Tooltip */
QToolTip {
    color: #ffffff;
    background-color: rgba(33, 37, 43, 180);
    border: 1px solid rgb(44, 49, 58);
    background-image: none;
    background-position: left center;
    background-repeat: no-repeat;
    border: none;
    border-left: 2px solid rgb(135, 148, 175);
    text-align: left;
    padding-left: 8px;
    margin: 0px;
}

/* Bg App */
#bgApp {
    background-color: rgb(40, 44, 52);
    border: 1px solid rgb(44, 49, 58);
}

/* /////////////////////////////////////////////////////////////////////////////////////////////////*/
/* QTreeView */
QTreeView {
    border: none;
}
QTreeView {
    selection-color:transparent;
}

QTreeView::item {
    background: solid rgb(40, 44, 52);
}

QTreeView::item:selected {
    background: 3px solid rgb(62, 67, 79);
    color: solid rgb(221, 221, 221);
    border: 1px solid rgb(40, 43, 51);
    border-left: 0px;
    border-right: 0px;
}
QTreeView::item:hover {
    background: 3px solid rgb(75, 82, 96);
}
QTreeView::item:hover:selected {
    background: 3px solid rgb(76, 82, 96);
}
QTreeView::item:focus {
    background: solid rgb(62, 67, 79);
}
QTreeView::item:focus:selected {
    background: solid rgb(76, 82, 96);
}


QTreeView::indicator:unchecked {
    border: 0px;
    background: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
}
QTreeView::indicator:checked {
    border: 0px;
    background: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
    background-image: url(:/icons/images/icons/cil-check-alt.png);
}
QTreeView::indicator:indeterminate {
    border: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
    background: solid rgb(34, 38, 45);
}

/* /////////////////////////////////////////////////////////////////////////////////////////////////*/
QTableView:item {
    background: transparent;
}
QTableView::indicator:unchecked {
    border: 0px;
    background: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
}
QTableView::indicator:checked {
    border: 0px;
    background: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
    background-image: url(:/icons/images/icons/cil-check-alt.png);
}
QTableView::indicator:indeterminate {
    border: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
    background: solid rgb(33, 37, 43);
}


QCheckBox::indicator:unchecked {
    border: 0px;
    background: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
}
QCheckBox::indicator:checked {
    border: 0px;
    background: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
    background-image: url(:/icons/images/icons/cil-check-alt.png);
}
QCheckBox::indicator:indeterminate {
    border: 3px solid rgb(52, 59, 72);
    border-radius: 2px;
    background: solid rgb(33, 37, 43);
}

/* /////////////////////////////////////////////////////////////////////////////////////////////////*/
#leftMenuBg {
    background-color: rgb(33, 37, 43);
}
#topLogo {
    background-color: rgb(33, 37, 43);
    background-image: url(:/images/images/images/PyDracula.png);
    background-position: centered;
    background-repeat: no-repeat;
}
#titleLeftApp { font: 63 12pt \ Segoe UI Semibold\ ; }
#titleLeftDescription { font: 8pt \ Segoe UI\ ; color: rgb(135, 148, 175); }

/* MENUS */
#topMenu .QPushButton {
    background-position: left center;
    background-repeat: no-repeat;
    border: none;
    border-left: 22px solid transparent;
    background-color: transparent;
    text-align: left;
    padding-left: 44px;
}
#topMenu .QPushButton:hover {
    background-color: rgb(40, 44, 52);
}
#topMenu .QPushButton:pressed {
    background-color: rgb(189, 147, 249);
    color: rgb(255, 255, 255);
}
#bottomMenu .QPushButton {
    background-position: left center;
    background-repeat: no-repeat;
    border: none;
    border-left: 20px solid transparent;
    background-color:transparent;
    text-align: left;
    padding-left: 44px;
}
#bottomMenu .QPushButton:hover {
    background-color: rgb(40, 44, 52);
}
#bottomMenu .QPushButton:pressed {
    background-color: rgb(135, 148, 175);
    color: rgb(255, 255, 255);
}
#leftMenuFrame{
    border-top: 3px solid rgb(44, 49, 58);
}

/* Toggle Button */
#toggleButton {
    background-position: left center;
    background-repeat: no-repeat;
    border: none;
    border-left: 20px solid transparent;
    background-color: rgb(37, 41, 48);
    text-align: left;
    padding-left: 44px;
    color: rgb(113, 126, 149);
}
#toggleButton:hover {
    background-color: rgb(40, 44, 52);
}
#toggleButton:pressed {
    background-color: rgb(135, 148, 175);
}
/* Title Menu */
#titleRightInfo { padding-left: 10px; }


/* Extra Tab */
#extraLeftBox {
    background-color: rgb(44, 49, 58);
}
#extraTopBg{
    background-color: rgb(135, 148, 175)
}

/* Icon */
#extraIcon {
    background-position: center;
    background-repeat: no-repeat;
    background-image: url(:/icons/images/icons/icon_settings.png);
}

/* Label */
#extraLabel { color: rgb(255, 255, 255); }

/* Btn Close */
#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }
#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }
#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }

/* Extra Content */
#extraContent {
    border-top: 3px solid rgb(40, 44, 52);
}

/* Extra Top Menus */
#extraTopMenu .QPushButton {
    background-position: left center;
    background-repeat: no-repeat;
    border: none;
    border-left: 22px solid transparent;
    background-color:transparent;
    text-align: left;
    padding-left: 44px;
}
#extraTopMenu .QPushButton:hover {
    background-color: rgb(40, 44, 52);
}
#extraTopMenu .QPushButton:pressed {
    background-color: rgb(135, 148, 175);
    color: rgb(255, 255, 255);
}

/* Content App */
#contentTopBg {
    background-color: rgb(33, 37, 43);
}
#contentBottom{
    border-top: 3px solid rgb(44, 49, 58);
}

/* Top Buttons */
#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }
#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }
#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }

/* Theme Settings */
#extraRightBox { background-color: rgb(44, 49, 58); }
#themeSettingsTopDetail { background-color: rgb(135, 148, 175); }

/* Bottom Bar */
#bottomBar { background-color: rgb(44, 49, 58); }
#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }

/* CONTENT SETTINGS */
/* MENUS */
#contentSettings .QPushButton {
    background-position: left center;
    background-repeat: no-repeat;
    border: none;
    border-left: 22px solid transparent;
    background-color:transparent;
    text-align: left;
    padding-left: 44px;
}
#contentSettings .QPushButton:hover {
    background-color: rgb(40, 44, 52);
}
#contentSettings .QPushButton:pressed {
    background-color: rgb(135, 148, 175);
    color: rgb(255, 255, 255);
}

/* QTableWidget */
QTableView {
    background-color: transparent;
    padding: 10px;
    border-radius: 5px;
    gridline-color: rgb(44, 49, 58);
    border-bottom: 1px solid rgb(44, 49, 60);
}

QHeaderView::section{
    background-color: rgb(33, 37, 43);
    max-width: 30px;
    border: 1px solid rgb(44, 49, 58);
    border-style: none;
    border-bottom: 1px solid rgb(44, 49, 60);
    border-right: 1px solid rgb(44, 49, 60);
}
QTableView::horizontalHeader {
    background-color: rgb(33, 37, 43);
}
QHeaderView::section:horizontal {
    border: 1px solid rgb(33, 37, 43);
    background-color: rgb(33, 37, 43);
    padding-top: 3px;
    padding-bottom: 3px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
}
QHeaderView::section:vertical {
     border: 1px solid rgb(44, 49, 60);
}

/* LineEdit */
QLineEdit {
    background-color: rgb(33, 37, 43);
    border-radius: 5px;
    border: 2px solid rgb(33, 37, 43);
    padding-left: 10px;
    selection-color: rgb(255, 255, 255);
    selection-background-color: rgb(135, 148, 175);
}
QLineEdit:hover {
    border: 2px solid rgb(64, 71, 88);
}
QLineEdit:focus {
    border: 2px solid rgb(91, 101, 124);
}

/* PlainTextEdit */
QPlainTextEdit {
    background-color: rgb(27, 29, 35);
    border-radius: 5px;
    padding: 10px;
    selection-color: rgb(255, 255, 255);
    selection-background-color: rgb(135, 148, 175);
}
QPlainTextEdit QScrollBar:vertical {
    width: 8px;
}
QPlainTextEdit QScrollBar:horizontal {
    height: 8px;
}
QPlainTextEdit:hover {
    border: 2px solid rgb(64, 71, 88);
}
QPlainTextEdit:focus {
    border: 2px solid rgb(91, 101, 124);
}

/* ScrollBars */
QScrollBar:horizontal {
    border: none;
    background: rgb(52, 59, 72);
    height: 8px;
    margin: 0px 21px 0 21px;
    border-radius: 0px;
}
QScrollBar::handle:horizontal {
    background: rgb(135, 148, 175);
    min-width: 25px;
    border-radius: 4px
}
QScrollBar::add-line:horizontal {
    border: none;
    background: rgb(55, 63, 77);
    width: 20px;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    border: none;
    background: rgb(55, 63, 77);
    width: 20px;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
    background: none;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
QScrollBar:vertical {
    border: none;
    background: rgb(52, 59, 72);
    width: 8px;
    margin: 21px 0 21px 0;
    border-radius: 0px;
}
QScrollBar::handle:vertical {
    background: rgb(135, 148, 175);
    min-height: 25px;
    border-radius: 4px
}
QScrollBar::add-line:vertical {
    border: none;
    background: rgb(55, 63, 77);
    height: 20px;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    border: none;
    background: rgb(55, 63, 77);
    height: 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* CheckBox
QTableWidget::indicator:checked,
QTreeView::indicator:checked,*/

#matplotWidget .QCheckBox::indicator {
    border: 3px solid rgb(52, 59, 72);
    width: 15px;
    height: 15px;
    border-radius: 10px;
    background: rgb(44, 49, 60);
}

#matplotWidget .QCheckBox::indicator:hover {
    border: 3px solid rgb(58, 66, 81);
}

#matplotWidget .QCheckBox::indicator:checked {
    background: 3px solid rgb(52, 59, 72);
    border: 3px solid rgb(52, 59, 72);
    background-image: url(:/icons/images/icons/cil-check-alt.png);
}

/* RadioButton */
QRadioButton::indicator {
    border: 3px solid rgb(52, 59, 72);
    width: 15px;
    height: 15px;
    border-radius: 10px;
    background: rgb(44, 49, 60);
}
QRadioButton::indicator:hover {
    border: 3px solid rgb(58, 66, 81);
}
QRadioButton::indicator:checked {
    background: 3px solid rgb(94, 106, 130);
    border: 3px solid rgb(52, 59, 72);
}

/* ComboBox */
QComboBox {
    background-color: rgb(33, 37, 43);
    border-radius: 5px;
    border: 2px solid rgb(33, 37, 43);
    padding: 5px;
    padding-left: 10px;
}
QComboBox:hover{
    border: 2px solid rgb(64, 71, 88);
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left-width: 3px;
    border-left-color: rgba(39, 44, 54, 150);
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    background-image: url(:/icons/images/icons/cil-arrow-bottom.png);
    background-position: center;
    background-repeat: no-reperat;
}
QComboBox QAbstractItemView {
    color: rgb(135, 148, 175);
    background-color: rgb(33, 37, 43);
    padding: 10px;
    selection-background-color: rgb(39, 44, 54);
    selection-color: (27, 29, 35);
    selection-background-color: (27, 29, 35);
}

/* Sliders */
QSlider::groove:horizontal {
    border-radius: 5px;
    height: 10px;
    margin: 0px;
    background-color: rgb(52, 59, 72);
}
QSlider::groove:horizontal:hover {
    background-color: rgb(55, 62, 76);
}
QSlider::handle:horizontal {
    background-color: rgb(135, 148, 175);
    border: none;
    height: 10px;
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}
QSlider::handle:horizontal:hover {
    background-color: rgb(195, 155, 255);
}
QSlider::handle:horizontal:pressed {
    background-color: rgb(135, 148, 175);
}

QSlider::groove:vertical {
    border-radius: 5px;
    width: 10px;
    margin: 0px;
    background-color: rgb(52, 59, 72);
}
QSlider::groove:vertical:hover {
    background-color: rgb(55, 62, 76);
}
QSlider::handle:vertical {
    background-color: rgb(135, 148, 175);
    border: none;
    height: 10px;
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}
QSlider::handle:vertical:hover {
    background-color: rgb(195, 155, 255);
}
QSlider::handle:vertical:pressed {
    background-color: rgb(135, 148, 175);
}

/* CommandLinkButton */
QCommandLinkButton {
    color: rgb(135, 148, 175);
    border-radius: 5px;
    padding: 5px;
    color: rgb(255, 170, 255);
}
QCommandLinkButton:hover {
    color: rgb(255, 170, 255);
    background-color: rgb(44, 49, 60);
}
QCommandLinkButton:pressed {
    color: rgb(135, 148, 175);
    background-color: rgb(52, 58, 71);
}

/* Button */
#pagesContainer QPushButton {
    border: 2px solid rgb(52, 59, 72);
    border-radius: 5px;
    background-color: rgb(52, 59, 72);
}
#pagesContainer QPushButton:hover {
    background-color: rgb(57, 65, 80);
    border: 2px solid rgb(61, 70, 86);
}
#pagesContainer QPushButton:pressed {
    background-color: rgb(35, 40, 49);
    border: 2px solid rgb(43, 50, 61);
}
QTabWidget::pane { /* The tab widget frame */
    border: 2px solid rgb(44, 49, 58);
    background-color:  rgb(40, 44, 52);
}
QTabBar::tab {
    background-color: rgb(33, 37, 43);
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 5px;
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}

FormDialog {
    background-color: rgb(40, 44, 52);
    color: rgb(221, 221, 221);
    font: 10pt \ Segoe UI\ ;
}

FormDialog QPushButton {
    border: 2px solid rgb(52, 59, 72);
    border-radius: 5px;
    background-color: rgb(52, 59, 72);
    padding: 3px;
}
FormDialog QPushButton:hover {
    background-color: rgb(57, 65, 80);
    border: 2px solid rgb(61, 70, 86);
}
FormDialog QPushButton:pressed {
    background-color: rgb(35, 40, 49);
    border: 2px solid rgb(43, 50, 61);
}

QColorDialog {
    background-color: rgb(40, 44, 52);
    font: 10pt \ Segoe UI\ ;
}

QColorDialog QPushButton {
    background-color: rgb(52, 59, 72);
    border: 2px solid rgb(52, 59, 72);
    border-radius: 5px;
    padding: 3px;
}
QColorDialog QPushButton:hover {
    background-color: rgb(52, 59, 72);
    border: 2px solid rgb(61, 70, 86);
}
QColorDialog QPushButton:pressed {
    background-color: rgb(52, 59, 72);
    border: 2px solid rgb(43, 50, 61);
}

QColorDialog QSpinBox {
    background-color: rgb(40, 44, 52);
}
"""

MATPLOT_WIDGET_STYLESHEET = """
/* Tool Button */
QToolButton {
    background-position: left center;
    background-repeat: no-repeat;
    border-left: 20px solid transparent;
    background-color: rgb(40, 44, 52);
    border: 1px;
    border-radius: 5px;
    color: rgb(113, 126, 149);
}
QToolButton:hover {
    background-color: rgb(44, 49, 57);
    border: none;
}
QToolButton:pressed {
    background-color: rgb(23, 26, 30);
    border: none;
}
QToolButton:checked {
    background-color: rgb(23, 26, 30);
    border: none;
}
"""
