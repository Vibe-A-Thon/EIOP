import {test, expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

for (const viewport of [{width: 390, height: 844}, {width: 1440, height: 900}]) {
  test(`connection page non-functional checks at ${viewport.width}px`, async ({page}) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.setViewportSize(viewport);
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.goto('/');
    await expect(page.getByLabel('Access token', {exact: true})).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    expect(overflow).toBe(false);
    expect(errors).toEqual([]);
    const result = await new AxeBuilder({page}).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
    expect(result.violations.filter(v => ['serious', 'critical'].includes(v.impact)).map(v => v.id)).toEqual([]);
  });
}
