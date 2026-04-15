from Domain_1_Astronomy.image_module.preprocessing import ImagePreprocessor
from Domain_1_Astronomy.image_module.ml.backbone import BackboneFeatureExtractor
from Domain_1_Astronomy.image_module.engines.feature_engine import FeatureEngine
from Domain_1_Astronomy.image_module.engines.quantitative_engine import QuantitativeEngine
from Domain_1_Astronomy.image_module.engines.morphological_engine import MorphologicalEngine
from Domain_1_Astronomy.image_module.engines.space_analysis_engine import SpaceAnalysisEngine
from Domain_1_Astronomy.image_module.engines.segmentation_engine import SegmentationEngine
from Domain_1_Astronomy.image_module.engines.heatmap_engine import HeatmapEngine
from Domain_1_Astronomy.image_module.engines.ai_labelling_engine import AILabellingEngine
from Domain_1_Astronomy.image_module.engines.temporal_engine import TemporalEngine
from Domain_1_Astronomy.image_module.engines.anomaly_engine import AnomalyEngine

from Domain_1_Astronomy.image_module.visualization.overlay_generator import OverlayGenerator
from Domain_1_Astronomy.image_module.visualization.heatmap_generator import HeatmapGenerator
from Domain_1_Astronomy.image_module.visualization.star_map_renderer import StarMapRenderer
from Domain_1_Astronomy.image_module.visualization.annotation_renderer import AnnotationRenderer


class ImagePipeline:

    def __init__(self):

        self.preprocessor = ImagePreprocessor()
        self.backbone = BackboneFeatureExtractor()
        self.feature_engine = FeatureEngine(self.backbone)

        self.quantitative_engine = QuantitativeEngine()
        self.morphological_engine = MorphologicalEngine()
        self.space_engine = SpaceAnalysisEngine()
        self.segmentation_engine = SegmentationEngine()

        self.heatmap_engine = HeatmapEngine()
        self.ai_labelling_engine = AILabellingEngine()

        self.temporal_engine = TemporalEngine()
        self.anomaly_engine = AnomalyEngine()

        self.overlay_generator = OverlayGenerator()
        self.heatmap_generator = HeatmapGenerator()
        self.star_map_renderer = StarMapRenderer()
        self.renderer = AnnotationRenderer()

    # --------------------------------------------------
    # SINGLE IMAGE PROCESSING
    # --------------------------------------------------

    def process(self, image_url, metadata):

        image, tensor = self.preprocessor.process(image_url)

        features = self.feature_engine.extract_all_features(image, tensor)
        quantitative_metrics = self.quantitative_engine.analyze(image)
        morphological_metrics = self.morphological_engine.analyze(image)
        segmentation_metrics = self.segmentation_engine.analyze(image)

        # 🔥 Conditional Deep Space Detection
        title_text = metadata.get("title", "").lower()

        is_deep_space = any(word in title_text for word in [
            "galaxy", "nebula", "star cluster", "deep space", "supernova"
        ])

        if is_deep_space:
            space_metrics_full = self.space_engine.analyze(image)
            star_points = space_metrics_full.get("star_points")
            cluster_labels = space_metrics_full.get("cluster_labels")
            space_metrics = {
                "star_count": space_metrics_full["star_count"],
                "star_density": space_metrics_full["star_density"],
                "cluster_count": space_metrics_full["cluster_count"]
            }
        else:
            star_points = []
            cluster_labels = []
            space_metrics = {
                "star_count": 0,
                "star_density": 0,
                "cluster_count": 0
            }

        scientific_context = {
            "quantitative_metrics": quantitative_metrics,
            "morphological_metrics": morphological_metrics,
            "space_metrics": space_metrics,
            "segmentation_metrics": {
                "emission_percentage": segmentation_metrics["emission_percentage"],
                "dark_percentage": segmentation_metrics["dark_percentage"],
                "core_percentage": segmentation_metrics["core_percentage"],
                "core_luminosity_ratio": segmentation_metrics["core_luminosity_ratio"],
                "turbulence_index": segmentation_metrics["turbulence_index"]
            }
        }

        ai_output = self.ai_labelling_engine.label_image(
            image=image,
            scientific_context=scientific_context
        )

        heatmap = self.heatmap_engine.generate_heatmap(image)
        heatmap_overlay = self.heatmap_generator.overlay_heatmap(image, heatmap)

        segmentation_overlay = self.overlay_generator.draw_segmentation(
            image,
            segmentation_metrics["emission_mask"],
            segmentation_metrics["dark_mask"],
            segmentation_metrics["core_mask"]
        )

        saved_images = []

        original_np = self.overlay_generator.draw_boxes(image, [])
        original_path = self.renderer.save_image(original_np, prefix="original")
        saved_images.append(original_path)

        heatmap_path = self.renderer.save_image(heatmap_overlay, prefix="heatmap")
        saved_images.append(heatmap_path)

        segmentation_path = self.renderer.save_image(segmentation_overlay, prefix="segmentation")
        saved_images.append(segmentation_path)

        if is_deep_space:
            star_map_image = self.star_map_renderer.render(
                image,
                star_points,
                cluster_labels
            )
            star_map_path = self.renderer.save_image(star_map_image, prefix="star_map")
            saved_images.append(star_map_path)

        metadata_output = {
            "features": features,
            "quantitative_metrics": quantitative_metrics,
            "morphological_metrics": morphological_metrics,
            "space_metrics": space_metrics,
            "segmentation_metrics": {
                "emission_percentage": segmentation_metrics["emission_percentage"],
                "dark_percentage": segmentation_metrics["dark_percentage"],
                "core_percentage": segmentation_metrics["core_percentage"],
                "core_luminosity_ratio": segmentation_metrics["core_luminosity_ratio"],
                "turbulence_index": segmentation_metrics["turbulence_index"]
            },
            "ai_interpretation": ai_output,
            "saved_images": saved_images
        }

        self.renderer.save_metadata(metadata_output)

        return metadata_output

    # --------------------------------------------------
    # TEMPORAL COMPARISON
    # --------------------------------------------------

    def compare_results(self, previous_result, current_result):

        temporal_metrics = self.temporal_engine.compare(
            previous_result,
            current_result
        )

        anomaly_report = self.anomaly_engine.evaluate(
            temporal_metrics
        )

        return {
            "temporal_metrics": temporal_metrics,
            "anomaly_report": anomaly_report
        }