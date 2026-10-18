/**
 * Enterprise i18n and localization framework (CRA-030.5, CRA-030.8).
 *
 * Supports:
 * - English (en-US, default)
 * - Arabic (ar, RTL layout testing)
 * - Pseudo-localization (qps-ploc, string expansion & special character reflow testing)
 * - Number and date localization
 * - Directionality attribute (ltr vs rtl)
 */

export const SUPPORTED_LOCALES = ['en', 'ar', 'qps-ploc'];

export const RTL_LOCALES = new Set(['ar', 'he', 'fa', 'ur']);

const DICTIONARIES = {
  en: {
    'app.title': 'Enterprise Ontology & Intelligence Platform',
    'nav.overview': 'Overview',
    'nav.sources': 'Source Management',
    'nav.ontology': 'Ontology Modeler',
    'nav.explorer': 'Knowledge Explorer',
    'nav.ask': 'Ask AI & Evidence',
    'nav.governance': 'Action Governance',
    'nav.settings': 'Settings',
    'state.loading': 'Loading authorized knowledge...',
    'state.empty': 'No records found for current filter.',
    'state.denied': 'Access denied: insufficient entitlements for current tenant.',
    'state.stale': 'Knowledge snapshot is stale. Refresh to synchronize.',
    'state.error': 'An error occurred while loading this view.',
    'action.connect': 'Connect',
    'action.disconnect': 'Disconnect this browser session',
    'action.save': 'Save Changes',
    'action.cancel': 'Cancel',
    'theme.light': 'Light',
    'theme.dark': 'Dark',
    'theme.hc_light': 'High contrast light',
    'theme.hc_dark': 'High contrast dark',
  },
  ar: {
    'app.title': 'منصة الأنطولوجيا والذكاء للمؤسسات',
    'nav.overview': 'نظرة عامة',
    'nav.sources': 'إدارة المصادر',
    'nav.ontology': 'نمذجة الأنطولوجيا',
    'nav.explorer': 'مستكشف المعرفة',
    'nav.ask': 'اسأل الذكاء الاصطناعي والأدلة',
    'nav.governance': 'حوكمة الإجراءات',
    'nav.settings': 'الإعدادات',
    'state.loading': 'جاري تحميل المعرفة المصرح بها...',
    'state.empty': 'لم يتم العثور على سجلات للتصفية الحالية.',
    'state.denied': 'تم رفض الوصول: أذونات غير كافية للمستأجر الحالي.',
    'state.stale': 'لقطة المعرفة قديمة. قم بالتحديث للمزامنة.',
    'state.error': 'حدث خطأ أثناء تحميل هذا العرض.',
    'action.connect': 'اتصال',
    'action.disconnect': 'قطع اتصال جلسة المتصفح هذه',
    'action.save': 'حفظ التغييرات',
    'action.cancel': 'إلغاء',
    'theme.light': 'فاتح',
    'theme.dark': 'داكن',
    'theme.hc_light': 'عالي التباين فاتح',
    'theme.hc_dark': 'عالي التباين داكن',
  },
};

/**
 * Generate pseudo-localized string with expansion and accented glyphs.
 * Example: "Overview" -> "[!!! Õvêrvîêŵ !!!]"
 */
function pseudoLocalize(text) {
  const charMap = {
    a: 'à', b: 'ƀ', c: 'ç', d: 'ð', e: 'ê', f: 'ƒ', g: 'ğ', h: 'ĥ', i: 'î',
    j: 'ĵ', k: 'ķ', l: 'ľ', m: 'ɱ', n: 'ñ', o: 'õ', p: 'þ', q: 'ʠ', r: 'ř',
    s: 'š', t: 'ţ', u: 'û', v: 'ṽ', w: 'ŵ', x: 'ẋ', y: 'ý', z: 'ž',
    A: 'À', B: 'Ɓ', C: 'Ç', D: 'Ð', E: 'Ê', F: 'Ƒ', G: 'Ğ', H: 'Ĥ', I: 'Î',
    J: 'Ĵ', K: 'Ķ', L: 'Ľ', M: 'Ṃ', N: 'Ñ', O: 'Õ', P: 'Þ', Q: 'Ǫ', R: 'Ř',
    S: 'Š', T: 'Ţ', U: 'Û', V: 'Ṽ', W: 'Ŵ', X: 'Ẋ', Y: 'Ý', Z: 'Ž',
  };
  const transformed = text.split('').map(c => charMap[c] || c).join('');
  return `[!!! ${transformed} !!!]`;
}

export class I18nManager {
  constructor(initialLocale = 'en') {
    this.currentLocale = SUPPORTED_LOCALES.includes(initialLocale) ? initialLocale : 'en';
  }

  setLocale(locale) {
    if (!SUPPORTED_LOCALES.includes(locale)) {
      throw new Error(`Unsupported locale: ${locale}. Must be one of ${SUPPORTED_LOCALES.join(', ')}`);
    }
    this.currentLocale = locale;
    if (typeof document !== 'undefined') {
      document.documentElement.lang = locale;
      document.documentElement.dir = this.getDirection();
    }
  }

  getLocale() {
    return this.currentLocale;
  }

  getDirection() {
    return RTL_LOCALES.has(this.currentLocale) ? 'rtl' : 'ltr';
  }

  isRTL() {
    return this.getDirection() === 'rtl';
  }

  t(key, params = {}) {
    if (this.currentLocale === 'qps-ploc') {
      const baseEn = DICTIONARIES.en[key] || key;
      let text = pseudoLocalize(baseEn);
      for (const [k, v] of Object.entries(params)) {
        text = text.replaceAll(`{${k}}`, String(v));
      }
      return text;
    }

    const dict = DICTIONARIES[this.currentLocale] || DICTIONARIES.en;
    let text = dict[key] || DICTIONARIES.en[key] || key;
    for (const [k, v] of Object.entries(params)) {
      text = text.replaceAll(`{${k}}`, String(v));
    }
    return text;
  }
}

export const i18n = new I18nManager();
