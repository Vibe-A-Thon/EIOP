import test from 'node:test';
import assert from 'node:assert/strict';
import { I18nManager, SUPPORTED_LOCALES } from '../../src/i18n.js';

test('i18n manager default english and ltr', () => {
  const i18n = new I18nManager();
  assert.equal(i18n.getLocale(), 'en');
  assert.equal(i18n.getDirection(), 'ltr');
  assert.equal(i18n.isRTL(), false);
  assert.equal(i18n.t('nav.overview'), 'Overview');
});

test('i18n arabic locale enforces rtl layout', () => {
  const i18n = new I18nManager('ar');
  assert.equal(i18n.getLocale(), 'ar');
  assert.equal(i18n.getDirection(), 'rtl');
  assert.equal(i18n.isRTL(), true);
  assert.equal(i18n.t('nav.overview'), 'نظرة عامة');
});

test('i18n pseudo-locale expands strings and maintains test tags', () => {
  const i18n = new I18nManager('qps-ploc');
  assert.equal(i18n.getLocale(), 'qps-ploc');
  assert.equal(i18n.getDirection(), 'ltr');
  const localized = i18n.t('nav.overview');
  assert.match(localized, /^\[!!! .* !!!\]$/);
  // Verify length expansion for truncation/reflow testing
  assert.ok(localized.length > 'Overview'.length + 6);
});

test('i18n rejects unsupported locale', () => {
  const i18n = new I18nManager();
  assert.throws(() => i18n.setLocale('unsupported_xx'), /Unsupported locale/);
});
