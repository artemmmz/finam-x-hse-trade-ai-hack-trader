import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# ==========================================
# Конфигурации визуализаций (читаемый формат)
# ==========================================

@dataclass
class ChartConfig:
    """Базовая конфигурация для всех графиков"""
    title: str
    paper_bgcolor: str = "rgba(0,0,0,0)"
    plot_bgcolor: str = "rgba(0,0,0,0)"
    font_color: str = "#e6e1ff"
    margin: Dict[str, int] = None
    
    def __post_init__(self):
        if self.margin is None:
            self.margin = {"l": 20, "r": 20, "t": 40, "b": 20}

@dataclass
class ColorScheme:
    """Цветовые схемы для графиков"""
    primary: str = "#7c3aed"
    secondary: str = "#a78bfa"
    accent: str = "#10b981"
    danger: str = "#ef4444"
    warning: str = "#f59e0b"
    colors_qualitative: List[str] = None
    
    def __post_init__(self):
        if self.colors_qualitative is None:
            self.colors_qualitative = px.colors.qualitative.Set3

# ==========================================
# Специфичные конфигурации для каждого типа графика
# ==========================================

VISUALIZATION_CONFIGS = {
    "sunburst": {
        "type": "sunburst",
        "config": ChartConfig(
            title="Структура портфеля по секторам",
            margin={"l": 5, "r": 5, "t": 30, "b": 5}
        ),
        "colors": ColorScheme(),
        "trace_params": {
            "marker_colors": "colors_qualitative"
        }
    },
    
    "performance": {
        "type": "line",
        "config": ChartConfig(
            title="Динамика стоимости портфеля",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        ),
        "colors": ColorScheme(),
        "traces": {
            "portfolio": {
                "name": "Портфель",
                "line_color": "primary",
                "line_width": 3
            },
            "benchmark": {
                "name": "Бенчмарк", 
                "line_color": "secondary",
                "line_width": 2,
                "line_dash": "dash"
            }
        }
    },
    
    "market_scanner": {
        "type": "table",
        "config": ChartConfig(
            title="",
            margin={"l": 0, "r": 0, "t": 0, "b": 0}
        ),
        "table_styles": {
            "header": {
                "fill_color": "#1f1f1f",
                "align": "left",
                "font": {"color": "white", "size": 12}
            },
            "cells": {
                "fill_color": "#2d2d2d", 
                "align": "left",
                "font": {"color": "white", "size": 11}
            }
        }
    },
    
    "technical_analysis": {
        "type": "candlestick",
        "config": ChartConfig(
            title="Технический анализ {symbol}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        ),
        "colors": ColorScheme(),
        "indicators": {
            "sma_20": {"color": "warning", "width": 1},
            "sma_50": {"color": "danger", "width": 1},
            "support": {"color": "accent", "dash": "dash"},
            "resistance": {"color": "danger", "dash": "dash"}
        }
    },
    
    "rsi": {
        "type": "line", 
        "config": ChartConfig(
            title="Индикатор RSI (Relative Strength Index)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        ),
        "colors": ColorScheme(),
        "levels": {
            "overbought": {"value": 70, "color": "danger", "text": "Перекупленность"},
            "oversold": {"value": 30, "color": "accent", "text": "Перепроданность"},
            "middle": {"value": 50, "color": "secondary", "text": ""}
        }
    }
}

# ==========================================
# Движок визуализаций
# ==========================================

class UniversalVisualizationEngine:
    def __init__(self):
        self.configs = VISUALIZATION_CONFIGS
        self.default_colors = ColorScheme()
    
    def create_chart(self, chart_type: str, data: Dict[str, Any], **kwargs) -> go.Figure:
        """
        Универсальный метод создания графиков
        
        Args:
            chart_type: Тип графика (sunburst, performance, technical_analysis, etc.)
            data: Данные для графика в структурированном формате
            **kwargs: Дополнительные параметры
        """
        if chart_type not in self.configs:
            raise ValueError(f"Unknown chart type: {chart_type}. Available: {list(self.configs.keys())}")
        
        config = self.configs[chart_type]
        method_name = f"_create_{chart_type}"
        
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(data, config, **kwargs)
        else:
            return self._create_generic_chart(data, config, **kwargs)
    
    def _create_sunburst(self, data: Dict, config: Dict, **kwargs) -> go.Figure:
        """Создание sunburst диаграммы"""
        portfolio = data.get("portfolio", [])
        
        sectors = {}
        for position in portfolio:
            sector = position.sector
            sectors[sector] = sectors.get(sector, 0) + position.weight
        
        labels = list(sectors.keys())
        parents = [""] * len(labels)
        values = list(sectors.values())
        
        for position in portfolio:
            labels.append(position.symbol)
            parents.append(position.sector)
            values.append(position.weight)
        
        colors = getattr(self.default_colors, config["trace_params"]["marker_colors"])
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors)
        ))
        
        self._apply_layout(fig, config["config"], **kwargs)
        return fig
    
    def _create_performance(self, data: Dict, config: Dict, **kwargs) -> go.Figure:
        """График производительности"""
        portfolio_data = data.get("portfolio_data")
        benchmark_data = data.get("benchmark_data")
        
        fig = go.Figure()
        
        # Портфель
        portfolio_config = config["traces"]["portfolio"]
        fig.add_trace(go.Scatter(
            x=portfolio_data['datetime'],
            y=portfolio_data['value'],
            name=portfolio_config["name"],
            line=dict(
                color=getattr(self.default_colors, portfolio_config["line_color"]),
                width=portfolio_config["line_width"]
            )
        ))
        
        # Бенчмарк
        if benchmark_data is not None:
            benchmark_config = config["traces"]["benchmark"]
            fig.add_trace(go.Scatter(
                x=benchmark_data['datetime'],
                y=benchmark_data['value'],
                name=benchmark_config["name"],
                line=dict(
                    color=getattr(self.default_colors, benchmark_config["line_color"]),
                    width=benchmark_config["line_width"],
                    dash=benchmark_config.get("line_dash")
                )
            ))
        
        self._apply_layout(fig, config["config"], **kwargs)
        fig.update_layout(
            xaxis_title="Дата",
            yaxis_title="Стоимость"
        )
        return fig
    
    def _create_technical_analysis(self, data: Dict, config: Dict, **kwargs) -> go.Figure:
        """Технический анализ"""
        historical_data = data.get("historical_data")
        indicators = data.get("indicators", {})
        symbol = data.get("symbol", "")
        
        fig = go.Figure()
        
        # Свечной график
        fig.add_trace(go.Candlestick(
            x=historical_data['datetime'],
            open=historical_data['open'],
            high=historical_data['high'],
            low=historical_data['low'],
            close=historical_data['close'],
            name=f"{symbol} Цены"
        ))
        
        # Индикаторы
        for indicator, params in config["indicators"].items():
            if indicator in indicators and indicators[indicator]:
                if indicator.startswith('sma_'):
                    values = [indicators[indicator]] * len(historical_data)
                    fig.add_trace(go.Scatter(
                        x=historical_data['datetime'],
                        y=values,
                        name=indicator.upper(),
                        line=dict(
                            color=getattr(self.default_colors, params["color"]),
                            width=params["width"]
                        )
                    ))
                elif indicator in ['support', 'resistance']:
                    fig.add_hline(
                        y=indicators[indicator],
                        line_dash=params["dash"],
                        line_color=getattr(self.default_colors, params["color"]),
                        annotation_text=indicator.capitalize()
                    )
        
        chart_config = config["config"]
        chart_config.title = chart_config.title.format(symbol=symbol)
        self._apply_layout(fig, chart_config, **kwargs)
        fig.update_layout(
            xaxis_title="Дата",
            yaxis_title="Цена"
        )
        return fig
    
    def _create_generic_chart(self, data: Dict, config: Dict, **kwargs) -> go.Figure:
        """Универсальный метод для создания графиков"""
        # Здесь можно добавить логику для других типов графиков
        raise NotImplementedError(f"Chart type generic creation not implemented")
    
    def _apply_layout(self, fig: go.Figure, chart_config: ChartConfig, **kwargs):
        """Применение настроек layout"""
        layout_updates = {
            "title": chart_config.title,
            "paper_bgcolor": chart_config.paper_bgcolor,
            "plot_bgcolor": chart_config.plot_bgcolor,
            "font": dict(color=chart_config.font_color),
            "margin": chart_config.margin
        }
        
        # Обновление из kwargs
        layout_updates.update(kwargs.get('layout_updates', {}))
        
        fig.update_layout(**layout_updates)

# ==========================================
# Использование
# ==========================================

# Примеры использования:
def examples():
    engine = UniversalVisualizationEngine()
    
    # 1. Sunburst диаграмма
    sunburst_data = {
        "portfolio": portfolio_list  # Ваш список PortfolioPosition
    }
    fig1 = engine.create_chart("sunburst", sunburst_data)
    
    # 2. График производительности
    performance_data = {
        "portfolio_data": portfolio_df,
        "benchmark_data": benchmark_df
    }
    fig2 = engine.create_chart("performance", performance_data)
    
    # 3. Технический анализ
    technical_data = {
        "historical_data": price_data,
        "indicators": {
            "sma_20": 150.5,
            "sma_50": 148.2,
            "support": 145.0,
            "resistance": 155.0
        },
        "symbol": "AAPL"
    }
    fig3 = engine.create_chart("technical_analysis", technical_data)

# Автоматизация для LLM
def create_visualization_automation(chart_type: str, input_data: Dict) -> Dict:
    """
    Функция для автоматического использования LLM
    
    Args:
        chart_type: Тип графика
        input_data: Входные данные в формате словаря
        
    Returns:
        Dict с информацией для создания графика
    """
    return {
        "chart_type": chart_type,
        "required_data": get_required_data_structure(chart_type),
        "config": VISUALIZATION_CONFIGS.get(chart_type, {}),
        "input_data_sample": input_data
    }

def get_required_data_structure(chart_type: str) -> Dict:
    """Возвращает структуру необходимых данных для каждого типа графика"""
    structures = {
        "sunburst": {
            "portfolio": "List[PortfolioPosition] - список позиций портфеля"
        },
        "performance": {
            "portfolio_data": "DataFrame с колонками ['datetime', 'value']",
            "benchmark_data": "Optional[DataFrame] с колонками ['datetime', 'value']" 
        },
        "technical_analysis": {
            "historical_data": "DataFrame с OHLC данными",
            "indicators": "Dict с техническими индикаторами",
            "symbol": "str - тикер инструмента"
        }
    }
    return structures.get(chart_type, {})