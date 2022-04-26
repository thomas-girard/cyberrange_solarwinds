import psutil
from psutil import AccessDenied
import sys, os
from fnv1a import FNV1a


def create_dico_process():
    """
    Get all process name and return a dictionary
    """

    dico_process =  {}
    for proc in psutil.process_iter():
        try:
            dico_process[proc.name().split(".")[0].lower()] = proc.pid # it's necessary to split in order to remove potentially ".exe"

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return dico_process

def create_dico_service():
    """
    Get all service name and return a dictionary
    """

    list_service = list(psutil.win_service_iter())
    dico_service = {}
    for name_instance in range(len(list_service)):
        dico_service[list_service[name_instance].name().lower()] = psutil.win_service_get(list_service[name_instance].name()).as_dict()
    return dico_service


def calculate_hash(string):
    """
    The hash is calculated by performing a FNV-1a 64bit hash of the lowercase string then XOR by 6605813339339102567.
    """

    hasher = FNV1a()
    return int(hasher.hash(string), 16) ^ 6605813339339102567

if __name__ == "__main__":

    dico_process = create_dico_process()

    dico_service = create_dico_service()

    hashList = [1475579823244607677, 2734787258623754862, 1368907909245890092, 16858955978146406642, 2597124982561782591, 2600364143812063535, 6195833633417633900, 2934149816356927366, 13029357933491444455, 15194901817027173566, 4821863173800309721, 13464308873961738403, 3320026265773918739, 12969190449276002545, 10657751674541025650, 12094027092655598256, 2760663353550280147, 8146185202538899243, 11818825521849580123, 11109294216876344399, 2797129108883749491, 3660705254426876796, 3890794756780010537, 3890769468012566366, 12709986806548166638, 14095938998438966337, 13611051401579634621, 18147627057830191163, 16423314183614230717, 11913842725949116895, 5449730069165757263, 12679195163651834776, 1614465773938842903, 11385275378891906608, 13693525876560827283, 17204844226884380288, 5984963105389676759, 17849680105131524334, 18246404330670877335, 292198192373389586, 14226582801651130532, 11266044540366291518, 6116246686670134098, 10734127004244879770, 18159703063075866524, 11771945869106552231, 9234894663364701749, 9061219083560670602, 8698326794961817906, 12790084614253405985, 16570804352575357627, 17097380490166623672, 16066522799090129502, 5219431737322569038, 15535773470978271326, 11073283311104541690, 3626142665768487764, 7810436520414958497, 4030236413975199654, 13316211011159594063, 13825071784440082496, 14480775929210717493, 14482658293117931546, 8473756179280619170, 15587050164583443069, 12718416789200275332, 9559632696372799208, 607197993339007484, 14513577387099045298, 4931721628717906635, 14079676299181301772, 3200333496547938354, 2589926981877829912, 8727477769544302060, 17939405613729073960, 17997967489723066537, 3778500091710709090, 8799118153397725683, 8873858923435176895, 13783346438774742614, 16112751343173365533, 17624147599670377042, 3425260965299690882, 16066651430762394116, 2380224015317016190, 13655261125244647696, 12027963942392743532, 576626207276463000, 9384605490088500348, 15092207615430402812, 6274014997237900919, 3320767229281015341, 7412338704062093516, 682250828679635420, 13014156621614176974, 18150909006539876521, 5587557070429522647, 12445177985737237804, 12445232961318634374, 17017923349298346219, 9333057603143916814, 541172992193764396, 10393903804869831898, 3413052607651207697, 3407972863931386250, 10545868833523019926, 521157249538507889, 3421213182954201407, 15039834196857999838, 3421197789791424393, 3413886037471417852, 17978774977754553159, 14243671177281069512, 14055243717250701608, 7315838824213522000, 14971809093655817917, 10336842116636872171, 6943102301517884811, 13544031715334011032, 397780960855462669, 13260224381505715848, 12785322942775634499, 17956969551821596225, 14256853800858727521, 8709004393777297355, 8129411991672431889, 15514036435533858158, 15997665423159927228, 10829648878147112121, 9149947745824492274, 13852439084267373191, 17633734304611248415, 13581776705111912829, 4578480846255629462, 8381292265993977266, 3796405623695665524, 5942282052525294911, 17984632978012874803, 3656637464651387014, 2717025511528702475, 10501212300031893463, 155978580751494388, 5183687599225757871, 10063651499895178962, 3575761800716667678, 4501656691368064027, 7701683279824397773, 10296494671777307979, 14630721578341374856, 6461429591783621719, 6508141243778577344, 4088976323439621041, 9531326785919727076, 10235971842993272939, 2478231962306073784, 9903758755917170407, 14710585101020280896, 2810460305047003196, 13611814135072561278, 2032008861530788751, 6491986958834001955, 27407921587843457, 2128122064571842954, 10484659978517092504, 2532538262737333146, 835151375515278827, 6088115528707848728, 4454255944391929578, 8478833628889826985, 10463926208560207521, 7080175711202577138, 8697424601205169055, 16130138450758310172, 7775177810774851294, 700598796416086955, 9007106680104765185, 506634811745884560, 18294908219222222902, 3588624367609827560, 9555688264681862794, 5415426428750045503, 3642525650883269872, 13135068273077306806, 3769837838875367802, 191060519014405309, 1682585410644922036, 7878537243757499832, 13799353263187722717, 1367627386496056834, 12574535824074203265, 16990567851129491937, 8994091295115840290, 13876356431472225791, 18392881921099771407, 5132256620104998637, 11801746708619571308, 14968320160131875803, 14868920869169964081, 106672141413120087, 79089792725215063, 16335643316870329598, 12343334044036541897, 5614586596107908838, 17291806236368054941, 3869935012404164040, 15267980678929160412, 1109067043404435916, 14111374107076822891, 3538022140597504361, 7175363135479931834, 3178468437029279937, 13599785766252827703, 6180361713414290679, 8612208440357175863, 8408095252303317471, 7982848972385914508, 8760312338504300643, 17351543633914244545, 7516148236133302073, 15114163911481793350, 7574774749059321801, 15457732070353984570, 16292685861617888592, 10374841591685794123, 3045986759481489935, 917638920165491138, 17109238199226571972, 5945487981219695001, 6827032273910657891, 8052533790968282297, 17574002783607647274, 3341747963119755850, 14193859431895170587, 15695338751700748390, 640589622539783622, 17683972236092287897, 17439059603042731363]

    try:
        detection_bool_process = False
        for process in [*dico_process]:
            hash_process = calculate_hash(process)
            if hash_process in hashList:
                print("Detection of a process in the list : ", process)
                detection_bool_process = True

        if detection_bool_process == False:
            print("No process is in the hash list !")
    except:
        pass

    try:
        detection_bool_service = False
        for service in [*dico_service]:
            hash_service = calculate_hash(process)
            if hash_service in hashList:
                print("Detection of a service in the list : ", process)
                detection_bool_service = True

                if dico_service[service]['pid'] is not None:
                    print("attempt to kill the service...")
                    try:
                        os.kill(dico_service[service]['pid'], 9)
                        print("Service killed ! ")
                    except:
                        print("Failure to stop service")

        if detection_bool_service == False:
            print("No service is in the hash list !")
    except:
        pass
    

    sys.exit(0)