def get_tab_stylesheet() -> str:
    return """
        QTabWidget::pane {
            border: none; /* Remove the border */
        }
        GE_TurnsBox {
            background-color: white;
        }
        GE_OriPickerBox {
            background-color: white;
        }
        QTabWidget::tab-bar:top {
            top: 1px;
        }
        QTabWidget::tab-bar:bottom {
            bottom: 1px;
        }
        QTabWidget::tab-bar:left {
            right: 1px;
        }
        QTabWidget::tab-bar:right {
            left: 1px;
        }
        QTabBar::tab {
            background: silver;
            font: 16pt "Calibri"; 
            color: black;
        }
        QTabBar::tab:selected {
            background: white;
        }
        QTabBar::tab:!selected:hover {
            background: #999;
        }
        QTabBar::tab:top:!selected {
            margin-top: 3px;
        }
        QTabBar::tab:bottom:!selected {
            margin-bottom: 3px;
        }
        QTabBar::tab:top, QTabBar::tab:bottom {
            min-width: 8ex;
            margin-right: -1px;
            padding: 5px 10px 5px 10px;
        }
        QTabBar::tab:top:selected {
            border-bottom-color: none;
        }
        QTabBar::tab:bottom:selected {
            border-top-color: none;
        }
        QTabBar::tab:left:!selected {
            margin-right: 3px;
        }
        QTabBar::tab:right:!selected {
            margin-left: 3px;
        }
        QTabBar::tab:left, QTabBar::tab:right {
            min-height: 8ex;
            margin-bottom: -1px;
            padding: 10px 5px 10px 5px;
        }
        QTabBar::tab:left:selected {
            border-left-color: none;
        }
        QTabBar::tab:right:selected {
            border-right-color: none;
        }
    """
