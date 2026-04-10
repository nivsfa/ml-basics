

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import os
    import pandas as pd
    return duckdb, mo, os


@app.cell
def _(mo):
    mo.md(
        r"""
        # 🗄️ SQL Interview Prep — Interactive Practice Notebook

        Practice SQL from basic `SELECT` statements all the way to advanced window functions,
        CTEs, and anomaly detection — all against a **real DuckDB database**.

        ## The Schema

        | Table | Description |
        |---|---|
        | `entity_metadata` | Site info: entity_id, category, sub_category |
        | `metrics_daily` | Daily visits per site + device type (Desktop/Mobile) |
        | `activity_logs` | Raw click events with timestamps and user IDs |
        | `attribute_performance` | Keyword/attribute volume by site, date, source |

        ## How to Use
        1. Read the question and hint
        2. Write your SQL in the editor
        3. Hit **Run** — your results appear instantly
        4. Reveal the reference solution when you're ready

        > **"The best way to learn SQL is to write a lot of SQL."**
        """
    )
    return


@app.cell
def _(duckdb, mo, os):
    DB_PATH = "db_exercises/analytics.db"
    if not os.path.exists(DB_PATH):
        mo.stop(True, mo.callout(
            mo.md(f"❌ **Database not found at `{DB_PATH}`.**\n\nRun your `setup_db()` script first to create and seed the database."),
            kind="danger"
        ))

    def run_query(sql: str, name: str = ""):
        """Execute SQL against the analytics DuckDB and return a DataFrame.
        If name is provided, saves the query as a txt to local_files/sql/<name>.txt."""
        try:
            con = duckdb.connect(DB_PATH, read_only=True)
            result = con.execute(sql).df()
            con.close()
            if name:
                save_dir = "local_files/sql"
                os.makedirs(save_dir, exist_ok=True)
                with open(f"{save_dir}/{name}.txt", "w") as f:
                    f.write(sql)
            return result, None
        except Exception as e:
            return None, str(e)

    # Quick connectivity test
    _test_df, _test_err = run_query("SELECT COUNT(*) AS n FROM entity_metadata", 'test')
    if _test_err:
        mo.stop(True, mo.callout(mo.md(f"❌ DB connection failed: `{_test_err}`"), kind="danger"))

    mo.callout(mo.md(f"✅ Connected to `{DB_PATH}` — `entity_metadata` has **{_test_df['n'][0]}** rows."), kind="success")
    return (run_query,)


@app.cell
def _(mo, run_query):
    # Schema explorer
    _tables = ["entity_metadata", "metrics_daily", "activity_logs", "attribute_performance"]
    _previews = {}
    for _t in _tables:
        _df, _ = run_query(f"SELECT * FROM {_t} LIMIT 3")
        _previews[_t] = _df

    mo.md(
        "## 🔍 Schema Preview\n\n" +
        "\n\n".join([
            f"### `{t}`\n" + (_previews[t].to_markdown(index=False) if _previews[t] is not None else "_error_")
            for t in _tables
        ])
    )
    return


@app.cell
def _(mo, run_query):
    def make_exercise(label, difficulty, question, hint, solution, default_sql="-- Write your SQL here\n"):
        """Return a marimo vstack representing one SQL exercise."""
        stars = {"Easy": "⭐", "Medium": "⭐⭐", "Hard": "⭐⭐⭐", "Expert": "⭐⭐⭐⭐"}
        header = mo.md(f"### {label} `[{difficulty} {stars.get(difficulty,'?')}]`\n\n{question}\n\n> 💡 **Hint:** {hint}")
        editor = mo.ui.code_editor(value=default_sql, language="sql")
        solution_toggle = mo.ui.switch(label="👁️ Show solution")

        def render(ed_val, show_sol):
            results_out = mo.md("_Run your query to see results._")
            if ed_val.strip() and ed_val.strip() != default_sql.strip():
                df, err = run_query(ed_val)
                if err:
                    results_out = mo.callout(mo.md(f"❌ **SQL Error:** `{err}`"), kind="danger")
                elif df is not None:
                    results_out = mo.vstack([
                        mo.callout(mo.md(f"✅ **{len(df)} row(s) returned**"), kind="success"),
                        mo.ui.table(df)
                    ])
            sol_out = mo.md(f"```sql\n{solution}\n```") if show_sol else mo.md("")
            return mo.vstack([header, editor, results_out, solution_toggle, sol_out])

        return render(editor.value, solution_toggle.value), editor, solution_toggle

    return


@app.cell
def _(os):
    def get_answer(name: str) -> str:
        path = f"local_files/sql/{name}.txt"
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return "-- Write your SQL here\n"
    return (get_answer,)


@app.cell
def _(mo):
    mo.md("""---\n## 📗 Section 1 — Basic SELECT & Filtering""")
    return


@app.cell
def _(mo):
    mo.md("""### Q1 `[Easy ⭐]`\n\nRetrieve all columns from `entity_metadata`.\n\n> 💡 **Hint:** Use `SELECT *`""")
    return


@app.cell
def _(get_answer, mo):
    q1_editor = mo.ui.code_editor(value=get_answer('q1'), language="sql")
    q1_editor
    return (q1_editor,)


@app.cell
def _(mo):
    q1_sol = mo.ui.switch(label="👁️ Show solution")
    return (q1_sol,)


@app.cell
def _(mo, q1_editor, q1_sol, run_query):
    _df, _err = run_query(q1_editor.value, 'q1') if q1_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q1_sol,
        mo.md("```sql\nSELECT * FROM entity_metadata;\n```") if q1_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q2 `[Easy ⭐]`\n\nList only the `entity_id` and `category` columns from `entity_metadata`.\n\n> 💡 **Hint:** Name the columns explicitly in SELECT.""")
    return


@app.cell
def _(get_answer, mo):
    q2_editor = mo.ui.code_editor(value=get_answer('q2'), language="sql")
    q2_editor
    return (q2_editor,)


@app.cell
def _(mo):
    q2_sol = mo.ui.switch(label="👁️ Show solution")
    return (q2_sol,)


@app.cell
def _(mo, q2_editor, q2_sol, run_query):
    _df, _err = run_query(q2_editor.value, 'q2') if q2_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q2_sol,
        mo.md("```sql\nSELECT entity_id, category FROM entity_metadata;\n```") if q2_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q3 `[Easy ⭐]`\n\nFind all entities in the `'E-commerce'` category.\n\n> 💡 **Hint:** Use `WHERE category = '...'`""")
    return


@app.cell
def _(get_answer, mo):
    q3_editor = mo.ui.code_editor(value=get_answer('q3'), language="sql")
    q3_editor
    return (q3_editor,)


@app.cell
def _(mo):
    q3_sol = mo.ui.switch(label="👁️ Show solution")
    return (q3_sol,)


@app.cell
def _(mo, q3_editor, q3_sol, run_query):
    _df, _err = run_query(q3_editor.value, 'q3') if q3_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q3_sol,
        mo.md("```sql\nSELECT *\nFROM entity_metadata\nWHERE category = 'E-commerce';\n```") if q3_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q4 `[Easy ⭐]`\n\nReturn distinct `device_type` values from `metrics_daily`.\n\n> 💡 **Hint:** `SELECT DISTINCT`""")
    return


@app.cell
def _(get_answer, mo):
    q4_editor = mo.ui.code_editor(value=get_answer('q4'), language="sql")
    q4_editor
    return (q4_editor,)


@app.cell
def _(mo):
    q4_sol = mo.ui.switch(label="👁️ Show solution")
    return (q4_sol,)


@app.cell
def _(mo, q4_editor, q4_sol, run_query):
    _df, _err = run_query(q4_editor.value, 'q4') if q4_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q4_sol,
        mo.md("```sql\nSELECT DISTINCT device_type FROM metrics_daily;\n```") if q4_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q5 `[Easy ⭐]`\n\nFind rows in `metrics_daily` where `visits > 100000` AND `device_type = 'Mobile'`.\n\n> 💡 **Hint:** Chain conditions with `AND`.""")
    return


@app.cell
def _(get_answer, mo):
    q5_editor = mo.ui.code_editor(value=get_answer('q5'), language="sql")
    q5_editor
    return (q5_editor,)


@app.cell
def _(mo):
    q5_sol = mo.ui.switch(label="👁️ Show solution")
    return (q5_sol,)


@app.cell
def _(mo, q5_editor, q5_sol, run_query):
    _df, _err = run_query(q5_editor.value, 'q5') if q5_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(10))]) if _df is not None else mo.md("_Write your query above._")),
        q5_sol,
        mo.md("```sql\nSELECT *\nFROM metrics_daily\nWHERE visits > 100000\n  AND device_type = 'Mobile'\nLIMIT 20;\n```") if q5_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""---\n## 📘 Section 2 — Aggregations & GROUP BY""")
    return


@app.cell
def _(mo):
    mo.md("""### Q6 `[Easy ⭐]`\n\nHow many total rows are in `metrics_daily`?\n\n> 💡 **Hint:** `COUNT(*)`""")
    return


@app.cell
def _(get_answer, mo):
    q6_editor = mo.ui.code_editor(value=get_answer('q6'), language="sql")
    q6_editor
    return (q6_editor,)


@app.cell
def _(mo):
    q6_sol = mo.ui.switch(label="👁️ Show solution")
    return (q6_sol,)


@app.cell
def _(mo, q6_editor, q6_sol, run_query):
    _df, _err = run_query(q6_editor.value, 'q6') if q6_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q6_sol,
        mo.md("```sql\nSELECT COUNT(*) AS total_rows FROM metrics_daily;\n```") if q6_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q7 `[Easy ⭐]`\n\nFor each `entity_id` in `metrics_daily`, compute the **total visits** across all dates and device types. Order by total visits descending.\n\n> 💡 **Hint:** `SUM()` + `GROUP BY` + `ORDER BY ... DESC`""")
    return


@app.cell
def _(get_answer, mo):
    q7_editor = mo.ui.code_editor(value=get_answer('q7'), language="sql")
    q7_editor
    return (q7_editor,)


@app.cell
def _(mo):
    q7_sol = mo.ui.switch(label="👁️ Show solution")
    return (q7_sol,)


@app.cell
def _(mo, q7_editor, q7_sol, run_query):
    _df, _err = run_query(q7_editor.value, 'q7') if q7_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q7_sol,
        mo.md("```sql\nSELECT entity_id,\n       SUM(visits) AS total_visits\nFROM metrics_daily\nGROUP BY entity_id\nORDER BY total_visits DESC;\n```") if q7_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q8 `[Medium ⭐⭐]`\n\nFor each `entity_id`, compute the **average daily visits** separately for Desktop and Mobile. Show entity_id, device_type, avg_visits. Round to 0 decimal places.\n\n> 💡 **Hint:** `GROUP BY entity_id, device_type` then `ROUND(AVG(visits), 0)`""")
    return


@app.cell
def _(get_answer, mo):
    q8_editor = mo.ui.code_editor(value=get_answer('q8'), language="sql")
    q8_editor
    return (q8_editor,)


@app.cell
def _(mo):
    q8_sol = mo.ui.switch(label="👁️ Show solution")
    return (q8_sol,)


@app.cell
def _(mo, q8_editor, q8_sol, run_query):
    _df, _err = run_query(q8_editor.value, 'q8') if q8_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q8_sol,
        mo.md("```sql\nSELECT entity_id,\n       device_type,\n       ROUND(AVG(visits), 0) AS avg_visits\nFROM metrics_daily\nGROUP BY entity_id, device_type\nORDER BY entity_id, device_type;\n```") if q8_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q9 `[Medium ⭐⭐]`\n\nWhich `entity_id` values had a **total visits (all devices) above 20,000,000** in 2025? List them with their totals.\n\n> 💡 **Hint:** Filter aggregations with `HAVING`. You may also need `WHERE event_date BETWEEN ...`""")
    return


@app.cell
def _(get_answer, mo):
    q9_editor = mo.ui.code_editor(value=get_answer('q9'), language="sql")
    q9_editor
    return (q9_editor,)


@app.cell
def _(mo):
    q9_sol = mo.ui.switch(label="👁️ Show solution")
    return (q9_sol,)


@app.cell
def _(mo, q9_editor, q9_sol, run_query):
    _df, _err = run_query(q9_editor.value, 'q9') if q9_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q9_sol,
        mo.md("```sql\nSELECT entity_id,\n       SUM(visits) AS total_visits\nFROM metrics_daily\nWHERE event_date BETWEEN '2025-01-01' AND '2025-12-31'\nGROUP BY entity_id\nHAVING SUM(visits) > 20000000\nORDER BY total_visits DESC;\n```") if q9_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q10 `[Medium ⭐⭐]`\n\nFor each `attribute_name` in `attribute_performance`, compute the total volume from `'Organic'` sources vs `'Paid'` sources **side by side** (pivot-style). Columns: `attribute_name`, `organic_volume`, `paid_volume`.\n\n> 💡 **Hint:** Use `SUM(CASE WHEN source_type = 'Organic' THEN volume ELSE 0 END)` to pivot.""")
    return


@app.cell
def _(get_answer, mo):
    q10_editor = mo.ui.code_editor(value=get_answer('q10'), language="sql")
    q10_editor
    return (q10_editor,)


@app.cell
def _(mo):
    q10_sol = mo.ui.switch(label="👁️ Show solution")
    return (q10_sol,)


@app.cell
def _(mo, q10_editor, q10_sol, run_query):
    _df, _err = run_query(q10_editor.value, 'q10') if q10_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q10_sol,
        mo.md("""```sql
    SELECT attribute_name,
        SUM(CASE WHEN source_type = 'Organic' THEN volume ELSE 0 END) AS organic_volume,
        SUM(CASE WHEN source_type = 'Paid'    THEN volume ELSE 0 END) AS paid_volume
    FROM attribute_performance
    GROUP BY attribute_name
    ORDER BY attribute_name;
    ```""") if q10_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""---\n## 📙 Section 3 — JOINs""")
    return


@app.cell
def _(mo):
    mo.md("""### Q11 `[Easy ⭐]`\n\nJoin `metrics_daily` with `entity_metadata` to add `category` to each metrics row. Show: entity_id, category, event_date, device_type, visits. Limit to 10 rows.\n\n> 💡 **Hint:** `INNER JOIN ... ON m.entity_id = e.entity_id`""")
    return


@app.cell
def _(get_answer, mo):
    q11_editor = mo.ui.code_editor(value=get_answer('q11'), language="sql")
    q11_editor
    return (q11_editor,)


@app.cell
def _(mo):
    q11_sol = mo.ui.switch(label="👁️ Show solution")
    return (q11_sol,)


@app.cell
def _(mo, q11_editor, q11_sol, run_query):
    _df, _err = run_query(q11_editor.value, 'q11') if q11_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q11_sol,
        mo.md("""```sql
    SELECT m.entity_id, e.category, m.event_date, m.device_type, m.visits
    FROM metrics_daily m
    INNER JOIN entity_metadata e ON m.entity_id = e.entity_id
    LIMIT 10;
    ```""") if q11_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q12 `[Medium ⭐⭐]`\n\nFor each **category** (from `entity_metadata`), compute the total visits across all sites in that category. Show category + total_visits, ordered by total descending.\n\n> 💡 **Hint:** JOIN first, then GROUP BY category.""")
    return


@app.cell
def _(get_answer, mo):
    q12_editor = mo.ui.code_editor(value=get_answer('q12'), language="sql")
    q12_editor
    return (q12_editor,)


@app.cell
def _(mo):
    q12_sol = mo.ui.switch(label="👁️ Show solution")
    return (q12_sol,)


@app.cell
def _(mo, q12_editor, q12_sol, run_query):
    _df, _err = run_query(q12_editor.value, 'q12') if q12_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q12_sol,
        mo.md("""```sql
    SELECT e.category,
        SUM(m.visits) AS total_visits
    FROM metrics_daily m
    INNER JOIN entity_metadata e ON m.entity_id = e.entity_id
    GROUP BY e.category
    ORDER BY total_visits DESC;
    ```""") if q12_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q13 `[Medium ⭐⭐]`\n\nFor each entity, show `entity_id`, `category`, and how many distinct `attribute_name` values exist for it in `attribute_performance`. Include entities with zero attributes (use LEFT JOIN).\n\n> 💡 **Hint:** `LEFT JOIN` + `COUNT(DISTINCT ap.attribute_name)`""")
    return


@app.cell
def _(get_answer, mo):
    q13_editor = mo.ui.code_editor(value=get_answer('q13'), language="sql")
    q13_editor
    return (q13_editor,)


@app.cell
def _(mo):
    q13_sol = mo.ui.switch(label="👁️ Show solution")
    return (q13_sol,)


@app.cell
def _(mo, q13_editor, q13_sol, run_query):
    _df, _err = run_query(q13_editor.value, 'q13') if q13_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q13_sol,
        mo.md("""```sql
    SELECT e.entity_id,
        e.category,
        COUNT(DISTINCT ap.attribute_name) AS num_attributes
    FROM entity_metadata e
    LEFT JOIN attribute_performance ap ON e.entity_id = ap.entity_id
    GROUP BY e.entity_id, e.category
    ORDER BY num_attributes DESC;
    ```""") if q13_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q14 `[Medium ⭐⭐]`\n\nFind `entity_id` values that appear in `metrics_daily` but **NOT** in `attribute_performance`.\n\n> 💡 **Hint:** Use `LEFT JOIN ... WHERE ap.entity_id IS NULL`, or `NOT IN (subquery)`, or `EXCEPT`.""")
    return


@app.cell
def _(get_answer, mo):
    q14_editor = mo.ui.code_editor(value=get_answer('q14'), language="sql")
    q14_editor
    return (q14_editor,)


@app.cell
def _(mo):
    q14_sol = mo.ui.switch(label="👁️ Show solution")
    return (q14_sol,)


@app.cell
def _(mo, q14_editor, q14_sol, run_query):
    _df, _err = run_query(q14_editor.value, 'q14') if q14_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q14_sol,
        mo.md("""```sql
    -- Approach 1: anti-join
    SELECT DISTINCT m.entity_id
    FROM metrics_daily m
    LEFT JOIN attribute_performance ap ON m.entity_id = ap.entity_id
    WHERE ap.entity_id IS NULL;

    -- Approach 2: EXCEPT
    SELECT DISTINCT entity_id FROM metrics_daily
    EXCEPT
    SELECT DISTINCT entity_id FROM attribute_performance;
    ```""") if q14_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""---\n## 📒 Section 4 — Subqueries & CTEs""")
    return


@app.cell
def _(mo):
    mo.md("""### Q15 `[Medium ⭐⭐]`\n\nUsing a subquery, find all rows in `metrics_daily` where visits exceed the **overall average visits**.\n\n> 💡 **Hint:** `WHERE visits > (SELECT AVG(visits) FROM metrics_daily)`""")
    return


@app.cell
def _(get_answer, mo):
    q15_editor = mo.ui.code_editor(value=get_answer('q15'), language="sql")
    q15_editor
    return (q15_editor,)


@app.cell
def _(mo):
    q15_sol = mo.ui.switch(label="👁️ Show solution")
    return (q15_sol,)


@app.cell
def _(mo, q15_editor, q15_sol, run_query):
    _df, _err = run_query(q15_editor.value, 'q15') if q15_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(10))]) if _df is not None else mo.md("_Write your query above._")),
        q15_sol,
        mo.md("""```sql
    SELECT *
    FROM metrics_daily
    WHERE visits > (SELECT AVG(visits) FROM metrics_daily)
    LIMIT 20;
    ```""") if q15_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q16 `[Medium ⭐⭐]`\n\nUsing a **CTE**, compute per-entity total visits, then select only those above the median total.\n\n> 💡 **Hint:** `WITH total_visits AS (...) SELECT ... FROM total_visits WHERE ...`""")
    return


@app.cell
def _(get_answer, mo):
    q16_editor = mo.ui.code_editor(value=get_answer('q16'), language="sql")
    q16_editor
    return (q16_editor,)


@app.cell
def _(mo):
    q16_sol = mo.ui.switch(label="👁️ Show solution")
    return (q16_sol,)


@app.cell
def _(mo, q16_editor, q16_sol, run_query):
    _df, _err = run_query(q16_editor.value, 'q16') if q16_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q16_sol,
        mo.md("""```sql
    WITH entity_totals AS (
        SELECT entity_id, SUM(visits) AS total_visits
        FROM metrics_daily
        GROUP BY entity_id
    ),
    med AS (
        SELECT MEDIAN(total_visits) AS med_visits FROM entity_totals
    )
    SELECT et.entity_id, et.total_visits
    FROM entity_totals et, med
    WHERE et.total_visits > med.med_visits
    ORDER BY et.total_visits DESC;
    ```""") if q16_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q17 `[Hard ⭐⭐⭐]`\n\nFind the **top-performing keyword** (by total volume) **for each entity**. Show entity_id, attribute_name, total_volume.\n\n> 💡 **Hint:** Aggregate volume per (entity, keyword), then use a CTE + `ROW_NUMBER()` or a correlated subquery to pick the top 1 per entity.""")
    return


@app.cell
def _(get_answer, mo):
    q17_editor = mo.ui.code_editor(value=get_answer('q17'), language="sql")
    q17_editor
    return (q17_editor,)


@app.cell
def _(mo):
    q17_sol = mo.ui.switch(label="👁️ Show solution")
    return (q17_sol,)


@app.cell
def _(mo, q17_editor, q17_sol, run_query):
    _df, _err = run_query(q17_editor.value, 'q17') if q17_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q17_sol,
        mo.md("""```sql
    WITH kw_totals AS (
        SELECT entity_id,
            attribute_name,
            SUM(volume) AS total_volume
        FROM attribute_performance
        GROUP BY entity_id, attribute_name
    ),
    ranked AS (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY total_volume DESC) AS rn
        FROM kw_totals
    )
    SELECT entity_id, attribute_name, total_volume
    FROM ranked
    WHERE rn = 1
    ORDER BY entity_id;
    ```""") if q17_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""---\n## 📕 Section 5 — Window Functions""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### 📚 Window Function Syntax

        ```sql
        function_name(column)
          OVER (
            [PARTITION BY partition_column]
            [ORDER BY sort_column]
            [ROWS/RANGE BETWEEN ...]
          )
        ```

        Common functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`,
        `SUM()`, `AVG()`, `MIN()`, `MAX()`, `NTILE(n)`.

        Window functions **do not collapse rows** — they add a new column computed across a window of rows.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""### Q18 `[Medium ⭐⭐]`\n\nFor each entity and device type in `metrics_daily`, compute a **7-day rolling average** of visits (ordered by date). Show entity_id, device_type, event_date, visits, rolling_avg_7d.\n\n> 💡 **Hint:** `AVG(visits) OVER (PARTITION BY entity_id, device_type ORDER BY event_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`""")
    return


@app.cell
def _(get_answer, mo):
    q18_editor = mo.ui.code_editor(value=get_answer('q18'), language="sql")
    q18_editor
    return (q18_editor,)


@app.cell
def _(mo):
    q18_sol = mo.ui.switch(label="👁️ Show solution")
    return (q18_sol,)


@app.cell
def _(mo, q18_editor, q18_sol, run_query):
    _df, _err = run_query(q18_editor.value, 'q18') if q18_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(15))]) if _df is not None else mo.md("_Write your query above._")),
        q18_sol,
        mo.md("""```sql
    SELECT entity_id,
        device_type,
        event_date,
        visits,
        ROUND(AVG(visits) OVER (
            PARTITION BY entity_id, device_type
            ORDER BY event_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 0) AS rolling_avg_7d
    FROM metrics_daily
    ORDER BY entity_id, device_type, event_date
    LIMIT 30;
    ```""") if q18_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q19 `[Medium ⭐⭐]`\n\nRank entities by their **total visits** per device type using `DENSE_RANK()`. Show device_type, entity_id, total_visits, rank_within_device.\n\n> 💡 **Hint:** Aggregate first in a CTE, then apply `DENSE_RANK() OVER (PARTITION BY device_type ORDER BY total_visits DESC)`.""")
    return


@app.cell
def _(get_answer, mo):
    q19_editor = mo.ui.code_editor(value=get_answer('q19'), language="sql")
    q19_editor
    return (q19_editor,)


@app.cell
def _(mo):
    q19_sol = mo.ui.switch(label="👁️ Show solution")
    return (q19_sol,)


@app.cell
def _(mo, q19_editor, q19_sol, run_query):
    _df, _err = run_query(q19_editor.value, 'q19') if q19_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q19_sol,
        mo.md("""```sql
    WITH agg AS (
        SELECT entity_id, device_type, SUM(visits) AS total_visits
        FROM metrics_daily
        GROUP BY entity_id, device_type
    )
    SELECT device_type,
        entity_id,
        total_visits,
        DENSE_RANK() OVER (PARTITION BY device_type ORDER BY total_visits DESC) AS rank_within_device
    FROM agg
    ORDER BY device_type, rank_within_device;
    ```""") if q19_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q20 `[Hard ⭐⭐⭐]`\n\nFor each entity + device type, compute the **day-over-day change in visits** (today minus yesterday). Show entity_id, device_type, event_date, visits, prev_visits, daily_delta.\n\n> 💡 **Hint:** `LAG(visits, 1) OVER (PARTITION BY entity_id, device_type ORDER BY event_date)`""")
    return


@app.cell
def _(get_answer, mo):
    q20_editor = mo.ui.code_editor(value=get_answer('q20'), language="sql")
    q20_editor
    return (q20_editor,)


@app.cell
def _(mo):
    q20_sol = mo.ui.switch(label="👁️ Show solution")
    return (q20_sol,)


@app.cell
def _(mo, q20_editor, q20_sol, run_query):
    _df, _err = run_query(q20_editor.value, 'q20') if q20_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(15))]) if _df is not None else mo.md("_Write your query above._")),
        q20_sol,
        mo.md("""```sql
    SELECT entity_id,
        device_type,
        event_date,
        visits,
        LAG(visits, 1) OVER (PARTITION BY entity_id, device_type ORDER BY event_date) AS prev_visits,
        visits - LAG(visits, 1) OVER (PARTITION BY entity_id, device_type ORDER BY event_date) AS daily_delta
    FROM metrics_daily
    ORDER BY entity_id, device_type, event_date
    LIMIT 30;
    ```""") if q20_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q21 `[Hard ⭐⭐⭐]`\n\nFor each entity, find the **single date** where Desktop visits were at their **all-time maximum**. Show entity_id, event_date, max_visits.\n\n> 💡 **Hint:** Use `RANK()` or `ROW_NUMBER()` partitioned by entity_id, ordered by visits DESC, then filter rank = 1.""")
    return


@app.cell
def _(get_answer, mo):
    q21_editor = mo.ui.code_editor(value=get_answer('q21'), language="sql")
    q21_editor
    return (q21_editor,)


@app.cell
def _(mo):
    q21_sol = mo.ui.switch(label="👁️ Show solution")
    return (q21_sol,)


@app.cell
def _(mo, q21_editor, q21_sol, run_query):
    _df, _err = run_query(q21_editor.value, 'q21') if q21_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q21_sol,
        mo.md("""```sql
    WITH ranked AS (
        SELECT entity_id,
            event_date,
            visits AS max_visits,
            ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY visits DESC) AS rn
        FROM metrics_daily
        WHERE device_type = 'Desktop'
    )
    SELECT entity_id, event_date, max_visits
    FROM ranked
    WHERE rn = 1
    ORDER BY entity_id;
    ```""") if q21_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""---\n## 📆 Section 6 — Date & Time""")
    return


@app.cell
def _(mo):
    mo.md("""### Q22 `[Easy ⭐]`\n\nFor each row in `metrics_daily`, extract the **month number** and **year**. Show entity_id, event_date, month_num, year_num.\n\n> 💡 **Hint:** `MONTH(event_date)` and `YEAR(event_date)` work in DuckDB.""")
    return


@app.cell
def _(get_answer, mo):
    q22_editor = mo.ui.code_editor(value=get_answer('q22'), language="sql")
    q22_editor
    return (q22_editor,)


@app.cell
def _(mo):
    q22_sol = mo.ui.switch(label="👁️ Show solution")
    return (q22_sol,)


@app.cell
def _(mo, q22_editor, q22_sol, run_query):
    _df, _err = run_query(q22_editor.value, 'q22') if q22_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(10))]) if _df is not None else mo.md("_Write your query above._")),
        q22_sol,
        mo.md("""```sql
    SELECT entity_id,
        event_date,
        MONTH(event_date) AS month_num,
        YEAR(event_date)  AS year_num
    FROM metrics_daily
    LIMIT 20;
    ```""") if q22_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q23 `[Medium ⭐⭐]`\n\nAggregate total visits by **month** for each entity. Show entity_id, year_month (formatted as `'YYYY-MM'`), total_visits.\n\n> 💡 **Hint:** `strftime(event_date, '%Y-%m')` or `DATE_TRUNC('month', event_date)` in DuckDB.""")
    return


@app.cell
def _(get_answer, mo):
    q23_editor = mo.ui.code_editor(value=get_answer('q23'), language="sql")
    q23_editor
    return (q23_editor,)


@app.cell
def _(mo):
    q23_sol = mo.ui.switch(label="👁️ Show solution")
    return (q23_sol,)


@app.cell
def _(mo, q23_editor, q23_sol, run_query):
    _df, _err = run_query(q23_editor.value, 'q23') if q23_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(15))]) if _df is not None else mo.md("_Write your query above._")),
        q23_sol,
        mo.md("""```sql
    SELECT entity_id,
        strftime(event_date, '%Y-%m') AS year_month,
        SUM(visits) AS total_visits
    FROM metrics_daily
    GROUP BY entity_id, year_month
    ORDER BY entity_id, year_month
    LIMIT 30;
    ```""") if q23_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q24 `[Medium ⭐⭐]`\n\nIn `activity_logs`, find all events that occurred within **5 seconds of each other** for the same `subject_id`. Hint: this is the bot-detection pattern (user 9999).\n\n> 💡 **Hint:** Self-join `activity_logs` on `subject_id`, then `EPOCH(b.occured_at) - EPOCH(a.occured_at) BETWEEN 0 AND 5`""")
    return


@app.cell
def _(get_answer, mo):
    q24_editor = mo.ui.code_editor(value=get_answer('q24'), language="sql")
    q24_editor
    return (q24_editor,)


@app.cell
def _(mo):
    q24_sol = mo.ui.switch(label="👁️ Show solution")
    return (q24_sol,)


@app.cell
def _(mo, q24_editor, q24_sol, run_query):
    _df, _err = run_query(q24_editor.value, 'q24') if q24_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(20))]) if _df is not None else mo.md("_Write your query above._")),
        q24_sol,
        mo.md("""```sql
    SELECT a.subject_id,
        a.occured_at AS event_a,
        b.occured_at AS event_b,
        EPOCH(b.occured_at) - EPOCH(a.occured_at) AS seconds_apart
    FROM activity_logs a
    JOIN activity_logs b
    ON a.subject_id = b.subject_id
    AND b.occured_at > a.occured_at
    AND EPOCH(b.occured_at) - EPOCH(a.occured_at) <= 5
    ORDER BY a.subject_id, a.occured_at
    LIMIT 20;
    ```""") if q24_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""---\n## 🔴 Section 7 — Advanced & Real-World Patterns""")
    return


@app.cell
def _(mo):
    mo.md("""### Q25 `[Hard ⭐⭐⭐]`\n\n**Mobile share %** — For each entity and month, compute what percentage of total visits came from Mobile (vs Desktop). Show entity_id, year_month, mobile_pct.\n\n> 💡 **Hint:** Use conditional SUM (CASE WHEN) divided by total SUM, multiplied by 100.""")
    return


@app.cell
def _(get_answer, mo):
    q25_editor = mo.ui.code_editor(value=get_answer('q25'), language="sql")
    q25_editor
    return (q25_editor,)


@app.cell
def _(mo):
    q25_sol = mo.ui.switch(label="👁️ Show solution")
    return (q25_sol,)


@app.cell
def _(mo, q25_editor, q25_sol, run_query):
    _df, _err = run_query(q25_editor.value, 'q25') if q25_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(15))]) if _df is not None else mo.md("_Write your query above._")),
        q25_sol,
        mo.md("""```sql
    SELECT entity_id,
        strftime(event_date, '%Y-%m') AS year_month,
        ROUND(
            100.0 * SUM(CASE WHEN device_type = 'Mobile' THEN visits ELSE 0 END)
            / NULLIF(SUM(visits), 0),
        2) AS mobile_pct
    FROM metrics_daily
    GROUP BY entity_id, year_month
    ORDER BY entity_id, year_month
    LIMIT 30;
    ```""") if q25_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q26 `[Hard ⭐⭐⭐]`\n\n**Detect bots** — Identify `subject_id` values in `activity_logs` that have **more than 5 events within any single minute**.\n\n> 💡 **Hint:** `DATE_TRUNC('minute', occured_at)` to bucket by minute, then `COUNT(*) > 5` with `HAVING`.""")
    return


@app.cell
def _(get_answer, mo):
    q26_editor = mo.ui.code_editor(value=get_answer('q26'), language="sql")
    q26_editor
    return (q26_editor,)


@app.cell
def _(mo):
    q26_sol = mo.ui.switch(label="👁️ Show solution")
    return (q26_sol,)


@app.cell
def _(mo, q26_editor, q26_sol, run_query):
    _df, _err = run_query(q26_editor.value, 'q26') if q26_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q26_sol,
        mo.md("""```sql
    SELECT subject_id,
        DATE_TRUNC('minute', occured_at) AS event_minute,
        COUNT(*) AS events_in_minute
    FROM activity_logs
    GROUP BY subject_id, event_minute
    HAVING COUNT(*) > 5
    ORDER BY events_in_minute DESC;
    ```""") if q26_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q27 `[Hard ⭐⭐⭐]`\n\n**Week-over-week growth** — For each entity + device type, compute the **% change in total weekly visits** vs the prior week. Show entity_id, device_type, week_start, weekly_visits, prev_week_visits, wow_growth_pct.\n\n> 💡 **Hint:** Aggregate to weekly level, then `LAG(...) OVER (PARTITION BY entity_id, device_type ORDER BY week_start)` to get prior week.""")
    return


@app.cell
def _(get_answer, mo):
    q27_editor = mo.ui.code_editor(value=get_answer('q27'), language="sql")
    q27_editor
    return (q27_editor,)


@app.cell
def _(mo):
    q27_sol = mo.ui.switch(label="👁️ Show solution")
    return (q27_sol,)


@app.cell
def _(mo, q27_editor, q27_sol, run_query):
    _df, _err = run_query(q27_editor.value, 'q27') if q27_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(20))]) if _df is not None else mo.md("_Write your query above._")),
        q27_sol,
        mo.md("""```sql
    WITH weekly AS (
        SELECT entity_id,
            device_type,
            DATE_TRUNC('week', event_date) AS week_start,
            SUM(visits) AS weekly_visits
        FROM metrics_daily
        GROUP BY entity_id, device_type, week_start
    ),
    with_lag AS (
        SELECT *,
            LAG(weekly_visits) OVER (
                PARTITION BY entity_id, device_type
                ORDER BY week_start
            ) AS prev_week_visits
        FROM weekly
    )
    SELECT entity_id,
        device_type,
        week_start,
        weekly_visits,
        prev_week_visits,
        ROUND(
            100.0 * (weekly_visits - prev_week_visits) / NULLIF(prev_week_visits, 0),
        2) AS wow_growth_pct
    FROM with_lag
    WHERE prev_week_visits IS NOT NULL
    ORDER BY entity_id, device_type, week_start
    LIMIT 30;
    ```""") if q27_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q28 `[Expert ⭐⭐⭐⭐]`\n\n**Traffic anomaly detection** — For each entity + device type, flag days where visits deviate more than **2 standard deviations** from the entity's mean. Show entity_id, device_type, event_date, visits, mean_visits, stddev_visits, z_score.\n\n> 💡 **Hint:** `AVG(visits) OVER (PARTITION BY ...)` and `STDDEV(visits) OVER (PARTITION BY ...)` — no ORDER BY needed (global window per partition). Then `z_score = (visits - mean) / stddev`.""")
    return


@app.cell
def _(get_answer, mo):
    q28_editor = mo.ui.code_editor(value=get_answer('q28'), language="sql")
    q28_editor
    return (q28_editor,)


@app.cell
def _(mo):
    q28_sol = mo.ui.switch(label="👁️ Show solution")
    return (q28_sol,)


@app.cell
def _(mo, q28_editor, q28_sol, run_query):
    _df, _err = run_query(q28_editor.value, 'q28') if q28_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(20))]) if _df is not None else mo.md("_Write your query above._")),
        q28_sol,
        mo.md("""```sql
    WITH stats AS (
        SELECT entity_id,
            device_type,
            event_date,
            visits,
            AVG(visits) OVER (PARTITION BY entity_id, device_type) AS mean_visits,
            STDDEV(visits) OVER (PARTITION BY entity_id, device_type) AS stddev_visits
        FROM metrics_daily
    )
    SELECT entity_id,
        device_type,
        event_date,
        visits,
        ROUND(mean_visits, 0)   AS mean_visits,
        ROUND(stddev_visits, 0) AS stddev_visits,
        ROUND((visits - mean_visits) / NULLIF(stddev_visits, 0), 2) AS z_score
    FROM stats
    WHERE ABS((visits - mean_visits) / NULLIF(stddev_visits, 0)) > 2
    ORDER BY ABS((visits - mean_visits) / NULLIF(stddev_visits, 0)) DESC
    LIMIT 30;
    ```""") if q28_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q29 `[Expert ⭐⭐⭐⭐]`\n\n**Funnel analysis** — A user 'session' is any sequence of clicks by the same `subject_id` where no gap between consecutive clicks exceeds 30 minutes. Assign a `session_id` to each click in `activity_logs`. Show subject_id, occured_at, entity_id, session_id.\n\n> 💡 **Hint:** Use `LAG` to get the previous event time per user, flag session breaks, then `SUM(is_new_session) OVER (PARTITION BY subject_id ORDER BY occured_at)` as a running session counter.""")
    return


@app.cell
def _(get_answer, mo):
    q29_editor = mo.ui.code_editor(value=get_answer('q29'), language="sql")
    q29_editor
    return (q29_editor,)


@app.cell
def _(mo):
    q29_sol = mo.ui.switch(label="👁️ Show solution")
    return (q29_sol,)


@app.cell
def _(mo, q29_editor, q29_sol, run_query):
    _df, _err = run_query(q29_editor.value, 'q29') if q29_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df.head(20))]) if _df is not None else mo.md("_Write your query above._")),
        q29_sol,
        mo.md("""```sql
    WITH lagged AS (
        SELECT subject_id,
            occured_at,
            entity_id,
            LAG(occured_at) OVER (PARTITION BY subject_id ORDER BY occured_at) AS prev_ts
        FROM activity_logs
    ),
    flagged AS (
        SELECT *,
            CASE
                WHEN prev_ts IS NULL
                    OR EPOCH(occured_at) - EPOCH(prev_ts) > 1800
                THEN 1 ELSE 0
            END AS is_new_session
        FROM lagged
    )
    SELECT subject_id,
        occured_at,
        entity_id,
        SUM(is_new_session) OVER (PARTITION BY subject_id ORDER BY occured_at) AS session_id
    FROM flagged
    ORDER BY subject_id, occured_at
    LIMIT 30;
    ```""") if q29_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""### Q30 `[Expert ⭐⭐⭐⭐]`\n\n**Retention cohort** — For each entity, define Q1 2025 (Jan–Mar) as the 'acquisition' period. Compute the **month-2 retention rate**: of all (entity, device_type) combinations active in Q1, what fraction were also active in April 2025?\n\n> 💡 **Hint:** CTE for Q1 active entities, CTE for April active entities, then LEFT JOIN and compute retention = COUNT(april_active) / COUNT(q1_active).""")
    return


@app.cell
def _(get_answer, mo):
    q30_editor = mo.ui.code_editor(value=get_answer('q30'), language="sql")
    q30_editor
    return (q30_editor,)


@app.cell
def _(mo):
    q30_sol = mo.ui.switch(label="👁️ Show solution")
    return (q30_sol,)


@app.cell
def _(mo, q30_editor, q30_sol, run_query):
    _df, _err = run_query(q30_editor.value, 'q30') if q30_editor.value.strip() != "-- Write your SQL here" else (None, None)
    mo.vstack([
        (mo.callout(mo.md(f"❌ `{_err}`"), kind="danger") if _err else
         mo.vstack([mo.callout(mo.md(f"✅ {len(_df)} rows"), kind="success"), mo.ui.table(_df)]) if _df is not None else mo.md("_Write your query above._")),
        q30_sol,
        mo.md("""```sql
    WITH q1_active AS (
        SELECT DISTINCT entity_id, device_type
        FROM metrics_daily
        WHERE event_date BETWEEN '2025-01-01' AND '2025-03-31'
        AND visits > 0
    ),
    april_active AS (
        SELECT DISTINCT entity_id, device_type
        FROM metrics_daily
        WHERE event_date BETWEEN '2025-04-01' AND '2025-04-30'
        AND visits > 0
    )
    SELECT
        COUNT(*) AS q1_combos,
        COUNT(a.entity_id) AS retained_in_april,
        ROUND(100.0 * COUNT(a.entity_id) / NULLIF(COUNT(*), 0), 2) AS retention_pct
    FROM q1_active q
    LEFT JOIN april_active a
    ON q.entity_id = a.entity_id
    AND q.device_type = a.device_type;
    ```""") if q30_sol.value else mo.md("")
    ])
    return


@app.cell
def _(mo):
    mo.md("""---\n## 🎮 Free Play — Write Any Query""")
    return


@app.cell
def _(mo):
    freeplay_editor = mo.ui.code_editor(
        value="-- Explore freely!\nSELECT * FROM entity_metadata;\n",
        language="sql",
        min_height=200
    )
    freeplay_editor
    return (freeplay_editor,)


@app.cell
def _(freeplay_editor, mo, run_query):
    _df, _err = run_query(freeplay_editor.value, 'freeplay')
    if _err:
        mo.callout(mo.md(f"❌ `{_err}`"), kind="danger")
    elif _df is not None:
        mo.vstack([
            mo.callout(mo.md(f"✅ **{len(_df)} row(s)**"), kind="success"),
            mo.ui.table(_df)
        ])
    else:
        mo.md("_No results yet._")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## 🏁 You've Reached the End!

        | Level | Questions | Skills Practiced |
        |---|---|---|
        | ⭐ Easy | Q1–Q8 | SELECT, WHERE, GROUP BY, HAVING |
        | ⭐⭐ Medium | Q9–Q19 | JOINs, CTEs, subqueries, window ranks |
        | ⭐⭐⭐ Hard | Q20–Q27 | LAG/LEAD, anomaly detection, time series |
        | ⭐⭐⭐⭐ Expert | Q28–Q30 | Z-scores, sessionization, cohort retention |

        Keep practicing — the best SQL engineers write thousands of queries. 🚀
        """
    )
    return


if __name__ == "__main__":
    app.run()
