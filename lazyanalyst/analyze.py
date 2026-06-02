import os
from . import loader
from . import schema
from . import quality
from . import cleaner
from . import eda
from . import visualizer
from . import features
from . import stats
from . import insights
from . import dashboard
from . import reporter

class LazyAnalystResult:
    """result object returned by analyze"""
    def __init__(self, cleaned_data_path, report_path, dashboard_path, cleaned_df):
        self.cleaned_data_path = cleaned_data_path
        self.report_path = report_path
        self.dashboard_path = dashboard_path
        self._cleaned_df = cleaned_df
    
    def dashboard(self):
        """opens dashboard.html in browser"""
        import webbrowser
        webbrowser.open(self.dashboard_path)
    
    def report(self):
        """opens report.html in browser"""
        import webbrowser
        webbrowser.open(self.report_path)
    
    def cleaned_data(self):
        """returns cleaned pandas DataFrame"""
        return self._cleaned_df


def analyze(filepath, build_dashboard=True, build_report=True):
    """runs full analysis pipeline"""
    
    # make sure outputs folder exists
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        print("[LazyAnalyst] Created outputs/ folder")
    
    # store all results in a dict
    all_results = {
        "filename": os.path.basename(filepath),
        "cleaned_df": None,
        "schema": None,
        "quality_report": None,
        "cleaning_actions": [],
        "eda_results": {},
        "features_created": [],
        "stats_results": [],
        "insights": []
    }
    
    # Module 1 - Loader
    print("\n[LazyAnalyst] Step 1/11 — Loading dataset...")
    try:
        df = loader.load(filepath)
        if df.empty:
            raise ValueError("Loaded dataframe is empty")
        all_results["original_df"] = df
    except Exception as e:
        print(f"[LazyAnalyst] Warning: loader failed — {e}. Skipping this step.")
        return None
    
    # Module 2 - Schema
    print("\n[LazyAnalyst] Step 2/11 — Detecting schema...")
    try:
        schema_dict = schema.detect(df)
        all_results["schema"] = schema_dict
    except Exception as e:
        print(f"[LazyAnalyst] Warning: schema detection failed — {e}. Skipping this step.")
        schema_dict = {}
        all_results["schema"] = {}
    
    # Module 3 - Quality
    print("\n[LazyAnalyst] Step 3/11 — Auditing data quality...")
    try:
        quality_report = quality.audit(df, schema_dict)
        all_results["quality_report"] = quality_report
    except Exception as e:
        print(f"[LazyAnalyst] Warning: quality audit failed — {e}. Skipping this step.")
        quality_report = {"score": 0, "missing": {}, "duplicates": {"count":0,"pct":0}, "outliers": {}, "invalid": []}
        all_results["quality_report"] = quality_report
    
    # Module 4 - Cleaner
    print("\n[LazyAnalyst] Step 4/11 — Cleaning dataset...")
    try:
        cleaned_df, actions = cleaner.clean(df, schema_dict, quality_report)
        all_results["cleaned_df"] = cleaned_df
        all_results["cleaning_actions"] = actions
    except Exception as e:
        print(f"[LazyAnalyst] Warning: cleaner failed — {e}. Skipping this step.")
        cleaned_df = df.copy()
        all_results["cleaned_df"] = cleaned_df
        all_results["cleaning_actions"] = []
    
    # Module 5 - EDA
    print("\n[LazyAnalyst] Step 5/11 — Running exploratory analysis...")
    try:
        eda_results = eda.run(cleaned_df, schema_dict)
        all_results["eda_results"] = eda_results
    except Exception as e:
        print(f"[LazyAnalyst] Warning: EDA failed — {e}. Skipping this step.")
        all_results["eda_results"] = {"numerical": {}, "categorical": {}, "correlation": {}}
    
    # Module 6 - Visualizer
    print("\n[LazyAnalyst] Step 6/11 — Generating visualizations...")
    try:
        visualizer.generate(cleaned_df, schema_dict)
    except Exception as e:
        print(f"[LazyAnalyst] Warning: visualizer failed — {e}. Skipping this step.")
    
    # Module 7 - Features
    print("\n[LazyAnalyst] Step 7/11 — Engineering features...")
    try:
        df_with_features, feat_list = features.engineer(cleaned_df, schema_dict)
        all_results["cleaned_df"] = df_with_features  # update df with new features
        all_results["features_created"] = feat_list
        # update schema for new columns? not necessary for v1
    except Exception as e:
        print(f"[LazyAnalyst] Warning: feature engineering failed — {e}. Skipping this step.")
        all_results["features_created"] = []
    
    # Module 8 - Stats
    print("\n[LazyAnalyst] Step 8/11 — Running statistical tests...")
    try:
        stats_results = stats.run(all_results["cleaned_df"], schema_dict)
        all_results["stats_results"] = stats_results
    except Exception as e:
        print(f"[LazyAnalyst] Warning: stats failed — {e}. Skipping this step.")
        all_results["stats_results"] = []
    
    # Module 9 - Insights
    print("\n[LazyAnalyst] Step 9/11 — Generating insights...")
    try:
        insight_list = insights.generate(
            all_results["eda_results"],
            all_results["stats_results"],
            all_results["quality_report"]
        )
        all_results["insights"] = insight_list
    except Exception as e:
        print(f"[LazyAnalyst] Warning: insights generation failed — {e}. Skipping this step.")
        all_results["insights"] = []
    
    # Module 10 - Dashboard - FIXED: use build_dashboard parameter
    dashboard_path = None
    if build_dashboard:
        print("\n[LazyAnalyst] Step 10/11 — Building dashboard...")
        dashboard_input = {
            "cleaned_df": all_results["cleaned_df"],
            "schema": all_results["schema"],
            "quality_report": all_results["quality_report"],
            "eda_results": all_results["eda_results"],
            "stats_results": all_results["stats_results"],
            "insights": all_results["insights"],
            "filename": all_results["filename"]
        }
        try:
            dashboard.build(dashboard_input)
            dashboard_path = "outputs/dashboard.html"
        except Exception as e:
            print(f"[LazyAnalyst] Warning: dashboard failed — {e}. Skipping this step.")
    else:
        print("\n[LazyAnalyst] Step 10/11 — Skipping dashboard (disabled)...")
    
    # Module 11 - Reporter - FIXED: use build_report parameter
    report_path = None
    if build_report:
        print("\n[LazyAnalyst] Step 11/11 — Generating HTML report...")
        report_input = {
            "cleaned_df": all_results["cleaned_df"],
            "schema": all_results["schema"],
            "quality_report": all_results["quality_report"],
            "cleaning_actions": all_results["cleaning_actions"],
            "eda_results": all_results["eda_results"],
            "features_created": all_results["features_created"],
            "stats_results": all_results["stats_results"],
            "insights": all_results["insights"],
            "filename": all_results["filename"]
        }
        try:
            reporter.build(report_input)
            report_path = "outputs/report.html"
        except Exception as e:
            print(f"[LazyAnalyst] Warning: reporter failed — {e}. Skipping this step.")
    else:
        print("\n[LazyAnalyst] Step 11/11 — Skipping report (disabled)...")
    
    print("\n[LazyAnalyst] Analysis complete!")
    print(f"[LazyAnalyst] Outputs saved to ./outputs/")
    
    # return result object
    cleaned_data_path = "outputs/cleaned_data.csv"
    return LazyAnalystResult(
        cleaned_data_path=cleaned_data_path,
        report_path=report_path if report_path else "",
        dashboard_path=dashboard_path if dashboard_path else "",
        cleaned_df=all_results["cleaned_df"]
    )
