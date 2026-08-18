# Support Case Insights

Analiza un CSV de tickets de soporte y genera un resumen de volumen, prioridad, categoría y tiempo promedio de resolución.

## Formato de entrada

El CSV debe incluir estas columnas: `id`, `opened_at`, `closed_at`, `status`, `priority`, `category`.

```csv
id,opened_at,closed_at,status,priority,category
INC-001,2026-08-01T09:00:00,2026-08-01T10:20:00,closed,high,access
```

## Uso

```powershell
python analyze_cases.py tickets.csv
```

Esta herramienta ayuda a responder preguntas operativas: qué categorías concentran más casos, qué prioridades crecen y cuánto tarda en cerrarse un ticket.
