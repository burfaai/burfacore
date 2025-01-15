from enum import Enum


class BurfaEnum(str, Enum):
    """_summary_: Base class for Burfa Enums."""

    @classmethod
    def get_choices(cls):
        """_summary_: Get choices for the enum."""
        return ((item.name, item.value) for item in cls)

    @classmethod
    def get_values(cls):
        """_summary_: Get values for the enum."""
        return (item.value for item in cls)


class Continent(BurfaEnum):
    """_summary_: Enum for Burfa Continent"""

    EUROPE = "europe"
    NORTH_AMERICA = "north america"
    SOUTH_AMERICA = "south america"
    AUSTRALIA = "australia"


class Country(BurfaEnum):
    """_summary_: Enum for Burfa DatasetCountry"""

    UNITED_KINGDOM = "united kingdom"
    UNITED_STATES = "united states"
    CANADA = "canada"
    AUSTRALIA = "australia"
    GERMANY = "germany"
    FRANCE = "france"
    ITALY = "italy"
    SPAIN = "spain"
    JAPAN = "japan"
    CHINA = "china"


class Language(BurfaEnum):
    """_summary_: Enum for Burfa Language"""

    ENGLISH = "english"
    FRENCH = "french"
    GERMAN = "german"
    SPANISH = "spanish"
    ITALIAN = "italian"
    JAPANESE = "japanese"
    CHINESE = "chinese"


class ComponentType(BurfaEnum):
    """_summary_: Enum for Burfa Component"""

    FEATURES = "features"
    GUIDELINES = "guidelines"
    DATASET = "dataset"
    MODEL = "model"


class Sector(BurfaEnum):
    """_summary_: Enum for Burfa Industry Sectors."""

    HEALTH = "health"
    MEDICAL = "medical"
    FINANCE = "finance"
    INSURANCE = "insurance"
    COPORATE_LAW = "corporate law"
    CRIMINAL_LAW = "criminal law"
    EDUCATION = "education"
    SURVEILLANCE = "surveillance"
    TRANSPORT = "transport"
    GOVERNMENT = "government"
    LAW_ENFORCEMENT = "law enforcement"
    MEDIA = "media"
    RETAIL = "retail"


class TaskType(BurfaEnum):
    """_summary_: Enum for Burfa job type."""

    GENERATION = "generation"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    CLASSIFICATION = "classification"
    RECOMMENDATION = "recommendation"
    MULTI_CLASSIFICATION = "multi-classification"


class ComplianceCategory(BurfaEnum):
    """_summary_: Enum for Burfa Guide Category"""

    BIAS = "bias"
    PRIVACY = "privacy"
    SECURITY = "security"
    FAIRNESS = "fairness"
    ROBUSTNESS = "robustness"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"
    EXPLAINABILITY = "explainability"
    GOVERNANCE = "governance"


class TrademarkType(BurfaEnum):
    """_summary_: Enum for Burfa Trademark Type"""

    LICENSED = "licensed"
    COMMERCIAL = "commercial"
    OPEN_SOURCE = "open source"


class EntityType(BurfaEnum):
    """_summary_: Enum for Burfa Entity Type"""

    DEVELOPER = "developer"
    DEPLOYER = "deployer"
    CONSUMER = "consumer"


class DatasetType(BurfaEnum):
    """_summary_: Burfa Dataset Type Enum."""

    TABULAR = "tabular"
    DATABASE = "database"
    DOCUMENT = "document"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"


class TabularFormat(BurfaEnum):
    """_summary_: Enum for Burfa Text Output Format"""

    CSV = "csv"
    JSON = "json"


class DatabaseFormat(BurfaEnum):
    """_summary_: Enum for Burfa Database Output Format"""

    SQLITE = "sqlite"
    JSON = "json"
    XLXS = "xlxs"


class DocumentFormat(BurfaEnum):
    """_summary_: Enum for Burfa Text Output Format"""

    TXT = "txt"
    DOCX = "docx"
    MARKDOWN = "markdown"
    PDF = "pdf"


class AudioFormat(BurfaEnum):
    """_summary_: Enum for Burfa Audio Output Format"""

    MP3 = "mp3"
    WAV = "wav"
    MIDI = "midi"


class ImageFormat(BurfaEnum):
    """_summary_: Enum for Burfa Image Output Format"""

    PNG = "png"
    JPG = "jpg"
    GIF = "gif"


class VideoFormat(BurfaEnum):
    """_summary_: Enum for Burfa Video Output Format"""

    MP4 = "mp4"
    MOV = "mov"
