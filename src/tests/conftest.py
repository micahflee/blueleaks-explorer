import sys
import os
import tempfile
import pytest

sys.path.append(os.path.dirname(sys.path[0]))
from app import app as flask_app

blueleaks_sites = [
    "211sfbay",
    "acprlea",
    "acticaz",
    "akorca",
    "alabamafusioncenter",
    "alabamalecc",
    "alertmidsouth",
    "aorca",
    "arictexas",
    "atlantahidta",
    "attackwa",
    "azhidta",
    "azorca",
    "bostonbric",
    "burlingamepolice",
    "cal-orca",
    "calema",
    "calstas",
    "cbaghidta",
    "ccroc",
    "chicagoheat",
    "chicagolandfsg",
    "ciacco",
    "cnoa3",
    "cnoatraining",
    "cnyorca",
    "coorca",
    "corca",
    "counterdrugtraining",
    "crimestopperslea",
    "cvchidta",
    "dediac",
    "dvicphila",
    "energysecuritycouncil",
    "eousa",
    "fbicahouston",
    "fbinaakansaswmissouri",
    "fbinaamichigan",
    "fbinaatexas",
    "fcpddoc",
    "flinttownshippolice",
    "fwintex",
    "gatlinburglec",
    "graorca",
    "hcsovcp",
    "hennepincountyshield",
    "hidtatraining",
    "hiorca",
    "houstonhidta",
    "houstonhidtatraining",
    "hpdlineup",
    "hpdretired",
    "icefishx",
    "ilcrime",
    "ileatraining",
    "iowaintex",
    "jerseyvillagepd",
    "jric",
    "kcpers",
    "kyorca",
    "lacleartraining",
    "lapdtraining",
    "leapsla",
    "losaltospdbc",
    "lupd",
    "mactf",
    "maorca",
    "membersfaithbased-isao",
    "memiac",
    "metrohoustonpolice",
    "mhidta",
    "miacx",
    "miacxold",
    "millvalleypolice",
    "miorca",
    "mlrin",
    "mnorca",
    "morciu",
    "mtorca",
    "mvpddoc",
    "mvpdtx",
    "ncric-history-good",
    "ncric",
    "ncricSteveBackup",
    "nctccounterdrug",
    "ndslic",
    "nehidta",
    "neorca",
    "nevadacyberexchange",
    "nhiac",
    "njuasi",
    "nmfisoa",
    "nmhidta",
    "nnorca",
    "nnric",
    "northtexasfusion",
    "northtexashidta",
    "novatopolicedept",
    "ntacnv",
    "nvhidta",
    "nymorca",
    "oaklandsheriffshield",
    "oaktac",
    "ociac",
    "okorca",
    "orcaid",
    "orcaor",
    "orocc",
    "otewg",
    "pchidta",
    "phillymostwanted",
    "pleasantonpolice",
    "prvihidta",
    "pspddoc",
    "publicsafetycadets",
    "repo",
    "richlandshield",
    "rlpsaroc",
    "rmhidta",
    "rockhillyorkcountyconnect",
    "ruasi",
    "ruralcountysummit",
    "sacrttac",
    "safecityabq",
    "safecityfw",
    "sanbrunopolice",
    "sccpca",
    "scgcsandiego",
    "sciic",
    "sdciaa",
    "sdfusion",
    "sdorca",
    "sduasi",
    "seattleshield",
    "Securitypartnership",
    "seffc",
    "semacp",
    "sfbay-infragard",
    "sicrime",
    "sltew",
    "snctc",
    "snorca",
    "sogtraining",
    "spottinglies",
    "stopabqgangs",
    "stopeasttexasgangs",
    "stophoustondrugs",
    "stoplubbockgangs",
    "stopnorthtexasgangs",
    "stopsanantoniogangs",
    "stopseattledrugs",
    "stopspokanegangs",
    "stopwesttexasgangs",
    "stxhidta",
    "sunnyvalebriefing",
    "swtxfusion",
    "terrorismtip",
    "texasorca",
    "tnoa",
    "twnsg",
    "unmpd",
    "usao",
    "utahsiac",
    "utorca",
    "vlnsn",
    "vslea",
    "wifusion",
    "wsorca",
]


@pytest.fixture()
def app():
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )

    yield flask_app


@pytest.fixture()
def blueleaks_path():
    """
    Create a temp dir for blueleaks_path, with an empty folder for each BlueLeaks site
    """
    d = tempfile.TemporaryDirectory()
    for site in blueleaks_sites:
        os.makedirs(os.path.join(d.name, site))
    os.environ["BLE_BLUELEAKS_PATH"] = d.name
    return d


@pytest.fixture()
def dbs_path():
    """
    Create a temp dir for dbs_path, with an fake sqlite3 file for each BlueLeaks file
    """
    d = tempfile.TemporaryDirectory()
    for site in blueleaks_sites:
        with open(os.path.join(d.name, f"{site}.sqlite3"), "wb") as f:
            f.write(b"not a real sqlite3 database")
    os.environ["BLE_DATABASES_PATH"] = d.name
    return d


@pytest.fixture()
def structures_paths():
    """
    Set environment variablse for structures_path, builtin_structures_path, and default_structures_path
    pointing to dirs in the source tree
    """
    builtin_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-builtin",
    )
    default_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-default",
    )

    # Create a temporary structures folder
    d = tempfile.mkdtemp()
    structures_path = os.path.join(d, "structures")
    os.makedirs(structures_path)
    # Copy data from builtin_structures into structures
    for f in os.listdir(builtin_structures_path):
        with open(os.path.join(builtin_structures_path, f), "rb") as src:
            with open(os.path.join(structures_path, f), "wb") as dst:
                dst.write(src.read())

    os.environ["BLE_STRUCTURES_PATH"] = structures_path
    os.environ["BLE_STRUCTURES_BUILTIN_PATH"] = builtin_structures_path
    os.environ["BLE_STRUCTURES_DEFAULT_PATH"] = default_structures_path
    return {
        "structures_path": structures_path,
        "builtin_structures_path": builtin_structures_path,
        "default_structures_path": default_structures_path,
    }


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
