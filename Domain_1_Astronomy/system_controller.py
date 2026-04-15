from Domain_1_Astronomy.query_module.query_processor import QueryProcessor
from Domain_1_Astronomy.search_module.search_engine import SearchEngine
from Domain_1_Astronomy.search_module.query_reliability_checker import QueryReliabilityChecker
from Domain_1_Astronomy.image_module.image_pipeline import ImagePipeline


class SystemController:

    def __init__(self):
        self.query_processor = QueryProcessor()
        self.reliability_checker = QueryReliabilityChecker()
        self.search_engine = SearchEngine()
        self.pipeline = ImagePipeline()

    # ----------------------------------------------------
    # MAIN ENTRY
    # ----------------------------------------------------

    def handle_query(self, user_query):

        # ------------------------------------------------
        # 1️⃣ QUERY PROCESSING (Grammar only)
        # ------------------------------------------------
        query_result = self.query_processor.process(user_query)

        if query_result["status"] == "rejected":
            return query_result

        corrected_query = query_result["corrected_query"]

        # ------------------------------------------------
        # 2️⃣ RELIABILITY CHECK (Does NASA have data?)
        # ------------------------------------------------
        validation = self.reliability_checker.validate(corrected_query)

        if not validation["is_valid"]:
            return {
                "status": "no_data_found",
                "query": corrected_query,
                "suggestions": validation["suggestions"]
            }

        # ------------------------------------------------
        # 3️⃣ DISPLAY BULK SEARCH RESULTS
        # ------------------------------------------------
        search_results = self.search_engine.search(
            keyword=corrected_query,
            limit=20
        )

        if not search_results:
            return {"error": "No scientific results found after filtering."}

        print("\nAvailable Scientific Results:")
        for i, item in enumerate(search_results):
            print(f"{i+1}. {item['title']} ({item['date_created']})")

        try:
            choice = int(input("Select image number: ")) - 1
        except ValueError:
            return {"error": "Invalid selection."}

        if choice < 0 or choice >= len(search_results):
            return {"error": "Invalid selection."}

        selected_item = search_results[choice]

        # ------------------------------------------------
        # 4️⃣ ASK ANALYSIS MODE
        # ------------------------------------------------
        mode = input("Choose analysis type (dynamic / timely): ").strip().lower()

        # ------------------------------------------------
        # DYNAMIC MODE
        # ------------------------------------------------
        if mode == "dynamic":

            analysis = self.pipeline.process(
                image_url=selected_item["image_url"],
                metadata=selected_item
            )

            return {
                "mode": "dynamic",
                "query": corrected_query,
                "analysis": analysis
            }

        # ------------------------------------------------
        # TIMELY MODE
        # ------------------------------------------------
        elif mode == "timely":

            year_start = input("Enter start year (YYYY): ").strip()
            year_end = input("Enter end year (YYYY): ").strip()

            time_series = self.search_engine.collect_time_series(
                keyword=corrected_query,
                year_start=year_start,
                year_end=year_end,
                limit=20
            )

            if not time_series:
                return {"error": "No data found in selected time range."}

            analyses = []

            for item in time_series:
                result = self.pipeline.process(
                    image_url=item["image_url"],
                    metadata=item
                )
                analyses.append(result)

            return {
                "mode": "timely",
                "query": corrected_query,
                "time_range": f"{year_start} - {year_end}",
                "analyses": analyses
            }

        else:
            return {"error": "Invalid analysis mode selected."}