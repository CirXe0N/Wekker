import { WekkerPage } from './app.po';

describe('wekker App', function() {
  let page: WekkerPage;

  beforeEach(() => {
    page = new WekkerPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
