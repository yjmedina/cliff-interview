from api.models import LicenseClassificationRequest, License
from api.classifier import LicenseClassifier
import pandas as pd
from typing import List


def classify_license(
        classifier: LicenseClassifier,
        request: LicenseClassificationRequest) -> License:
        classification = classifier.run(request.description)
        license = License(
                license_id=request.license_id,
                license_description=request.description,
                category=classification.category,
                explanation=classification.explanation,
                manually_validated=False
        )
        return license


def process_licenses(
        classifier: LicenseClassifier,
        input_file: str,
        output_file: str
    ) -> None:

    """Process licenses from input file and save to output file"""
    df = pd.read_csv(input_file)
    licenses: List[License] = []
    for _, row in df.iterrows():
        license_request = LicenseClassificationRequest(license_id=row['License ID'], description=row['License Description'])
        license = classify_license(classifier, license_request)
        print(license)
        licenses.append(license)
    
    pd_output = pd.DataFrame([li.model_dump() for li in licenses])
    pd_output.to_csv(output_file, index=False)


if __name__ == '__main__':
    from api.config import Settings
    settings = Settings()
    classifier = LicenseClassifier(settings.open_api_key)

    process_licenses(
        classifier,
        settings.input_licenses_csv,
        settings.output_licenses_csv
        )
