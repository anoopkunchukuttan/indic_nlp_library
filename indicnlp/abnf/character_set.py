# each language character set can be divided into for sets, m : modifiers like anuswar,  v : matras , V : independent
# vowels and CH: consonants. rest of the chararacters are treted as symbols

symbols = ") + * / , . : ; = > ] - _ | ~ % } { ( ["

HI_C = "क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न ऩ प फ ब भ म य र ऱ ल ळ ऴ व श ष स ह क़ ख़ ग़ ज़ ड़ ढ़ फ़ य़ ॸ ॹ ॺ ॻ ॼ ॽ ॾ ॿ"
HI_V = "ऄ अ आ इ ई उ ऊ ऋ ऌ ऍ ऎ ए ऐ ऑ ऒ ओ औ ॠ ॡ ॲ ॳ ॴ ॵ ॶ ॷ"
HI_v = "ऺ ऻ ा ि ी ु ू ृ ॄ ॅ ॆ े ै ॉ ॊ ो ौ ॎ ॏ ॕ ॖ ॗ ॢ ॣ "
HI_m = "ऀ ँ ं ः ऽ ़ "
HI_H = "् "
HI_digits = "०  १  २  ३  ४  ५  ६  ७  ८  ९"
HI_symbols = HI_digits + symbols + "। ॥ ॐ"

BN_C = "ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ ত থ দ ধ ন প ফ ব ভ ম য র ল শ ষ স হ ৎ ড় ঢ় য়ৰ ৱ "
BN_V = "অ আ ই ঈ উ ঊ ঋ ঌ এ ঐ ও ঔ ৠ ৡ "
BN_v = "া ি ী ু ূ ৃ ৄ ে ৈ ো ৌ ৗ ৢ ৣ "
BN_m = "ঀ ঁ ং ঃ ঽ ় "
BN_H = "্ "
BN_digits = "০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯ "
BN_symbols = BN_digits + symbols + "৲ ৳ ৴ ৵ ৶ ৷ ৸ ৹ ৺ ৻ ৼ ৽ ৾ "

GUR_C = "ਕ ਖ ਗ ਘ ਙ ਚ ਛ ਜ ਝ ਞ ਟ ਠ ਡ ਢ ਣ ਤ ਥ ਦ ਧ ਨ ਪ ਫ ਬ ਭ ਮ ਯ ਰ ਲ ਲ਼ ਵ ਸ਼ ਸ ਹ ਖ਼ ਗ਼ ਜ਼ ੜ ਫ਼ ੵ "
GUR_V = "ਅ ਆ ਇ ਈ ਉ ਊ ਏ ਐ ਓ ਔ ੲ ੳ"
GUR_v = "ਾ ਿ ੀ ੁ ੂ ੇ ੈ ੋ ੌ "
GUR_m = "ਁ ਂ ੰ ਃ ਼ ੰ ੱ "
GUR_H = "੍ "
GUR_digits = "੦  ੧  ੨  ੩  ੪  ੫  ੬  ੭  ੮  ੯"
GUR_symbols = GUR_digits + symbols + "ੴ ੶"

GU_C = "ક ખ ગ ઘ ઙ ચ છ જ ઝ ઞ ટ ઠ ડ ઢ ણ ત થ દ ધ ન પ ફ બ ભ મ ય ર લ ળ વ શ ષ સ હ ૹ"
GU_V = "અ આ ઇ ઈ ઉ ઊ ઋ ઌ ઍ એ ઐ ઑ ণ ত ૠ ૡ "
GU_v = "ા િ ી ુ ૂ ૃ ૄ ૅ ે ૈ ૉ ો ૌ ૢ ૣ "
GU_m = "ઁ ં ઃ ઽ ઼ "
GU_H = "્ "
GU_digits = "૦  ૧  ૨  ૩  ૪  ૫  ૬  ૭  ૮  ૯ "

GU_symbols = GU_digits + symbols + "ઓ ઔ ૐ ૤ ૥ ૰ ૱"

OR_C = "କ ଖ ଗ ଘ ଙ ଚ ଛ ଜ ଝ ଞ ଟ ଠ ଡ ଢ ଣ ତ ଥ ଦ ଧ ନ ପ ଫ ବ ଭ ମ ଯ ର ଲ ଳ ଵ ଶ ଷ ସ ହ ଡ଼ ଢ଼ ୟ ୱ "
OR_V = "ଅ ଆ ଇ ଈ ଉ ଊ ଋ ଌ ଏ ଐ ଓ ଔ ୠ ୡ "
OR_v = "ା ି ୀ ୁ ୂ ୃ ୄ େ ୈ ୋ ୌ ୖ ୗ ୢ ୣ"
OR_m = "ଁ ଂ ଃ ଽ ଼ "
OR_H = "୍ "
OR_digits = "୦  ୧  ୨  ୩  ୪  ୫  ୬  ୭  ୮  ୯"
OR_symbols = OR_digits + symbols + "଱ ୰ ୲ ୳ ୴ ୵ ୶ ୷ "

ML_C = 'ക ഖ ഗ ഘ ങ ച ഛ ജ ഝ ഞ ട ഠ ഡ ഢ ണ ത ഥ ദ ധ ന ഩ പ ഫ ബ ഭ മ യ ര റ ല ള ഴ വ ശ ഷ സ ഹ ഺ ൺ ൻ ർ ൽ ൾ ൿ'
ML_V = 'അ ആ ഇ ഈ ഉ ഊ ഋ ഌ എ ഏ ഐ ഒ ഓ ഔ ൟ ൠ ൡ '
ML_v = 'ാ ി ീ ു ൂ ൃ ൄ െ േ ൈ ൊ ോ ൌ ൗ ൢ ൣ '
ML_m = ' ഁ ം ഃ ഽ '
ML_H = '് '
ML_digit = '൦  ൧  ൨  ൩  ൪  ൫  ൬  ൭  ൮  ൯'
ML_symbols = symbols + ML_digit + ' ഀ ഄ  ഻ ഼   ൎ ൏  ൔ ൕ ൖ ൘ ൙ ൚ ൛ ൜ ൝ ൞  ൰ ൱ ൲ ൳ ൴ ൵ ൶ ൷ ൸ ൹ '

KN_C = "ಕ ಖ ಗ ಘ ಙ ಚ ಛ ಜ ಝ ಞ ಟ ಠ ಡ ಢ ಣ ತ ಥ ದ ಧ ನ ಪ ಫ ಬ ಭ ಮ ಯ ರ ಱ ಲ ಳ ವ ಶ ಷ ಸ ಹ ೞ"
KN_V = 'ಅ ಆ ಇ ಈ ಉ ಊ ಋ ಌ ಎ ಏ ಐ ಒ ಓ ಔ ೠ ೡ '
KN_v = 'ಾ ಿ ೀ ು ೂ ೃ ೄ ೆ ೇ ೈ ೊ ೋ ೌ ೕ ೖ ೢ ೣ '
KN_m = 'ಂ ಃ ಼ ಽ ೱ ೲ '
KN_H = '್ '
KN_digit = '೦ ೧  ೨  ೩  ೪  ೫  ೬  ೭  ೮  ೯ '
KN_symbols = symbols + KN_digit + 'ಀ ಁ ಄ ೅ ೉'

TA_C = 'க ங ச ஜ ஞ ட ண த ந ன ப ம ய ர ற ல ள ழ வ ஶ ஷ ஸ ஹ'
TA_V = 'அ ஆ இ ஈ உ ஊ எ ஏ ஐ ஒ ஓ ஔ '
TA_v = 'ா ி ீ ு ூ ெ ே ை ொ ோ ௌ '
TA_m = 'ஂ ஃ '
TA_H = '்'
TA_digit = '௦  ௧  ௨  ௩  ௪  ௫  ௬  ௭  ௮  ௯ '
TA_symbols = symbols + TA_digit + ' ஗  ஬  ஻ ஼ ஽  ௏ ௐ  ௗ ௘  ௛ ௞  ௰ ௱ ௲ ௳ ௴ ௵ ௶ ௷ ௸ ௹ ௺ '

TE_C = 'క ఖ గ ఘ ఙ చ ఛ జ ఝ ఞ ట ఠ డ ఢ ణ త థ ద ధ న ప ఫ బ భ మ య ర ఱ ల ళ ఴ వ శ ష స హ'
TE_V = 'అ ఆ ఇ ఈ ఉ ఊ ఋ ఌ ఎ ఏ ఐ ఒ ఓ ఔ ౠ ౡ'
TE_v = 'ా ి ీ ు ూ ృ ౄ ె ే ై ొ ో ౌ ౕ ౖ ౢ ౣ '
TE_m = 'ఀ ఁ ం ః ఽ '
TE_H = '్ '
TE_digit = '౦ ౧  ౨  ౩  ౪  ౫  ౬  ౭  ౮  ౯ '
TE_symbols = symbols + TE_digit + 'ౘ ౙ ౚ  ౷ ౸ ౹ ౺ ౻ ౼ ౽ ౾ ౿ '
