/*
 * Inventory Menu Views
 *
 * js/app/common/menu_views.js
 *
 * MENU VIEW ENTRY POINTS
 */

"use strict";


// Inventory Menu
class InventoryItemMenu extends MenuItem {
  get toggle() { return true; }

  constructor(options) {
    super(options);
  }

  onClickCallback(model) {
    App.viewFunctions.inventory(model);
  }
};


class InventoryParentMenu extends Menu {
  constructor(options) {
    super(options);
  }

  renderCallback(model) {
    return new InventoryItemMenu({model: model});
  }
};


class InventoryMenu extends Backbone.View {
  get el() { return 'div#content'; }

  constructor(options) {
    super(options);
  }

  initialize() {
    _.bindAll(this);
  }

  render() {
    let menu = new InventoryParentMenu({collection: this.collection});
    this.$el.append(menu.render().el);
  }
};


// Project Menu
class ProjectItemMenu extends MenuItem {
  get toggle() { return false; }

  constructor(options) {
    super(options);
  }

  onClickCallback(model) {
    App.viewFunctions.projects(model);
  }
};


class ProjectParentMenu extends Menu {
  constructor(options) {
    super(options);
  }

  renderCallback(model) {
    return new ProjectItemMenu({model: model});
  }
};


class ProjectMenu extends Backbone.View {
  get el() { return 'div#projects div.tab-choice-pane div.pane-nav'; }

  constructor(options) {
    super(options);
  }

  initialize() {
    _.bindAll(this);
  }

  render() {
    let menu = new ProjectParentMenu({collection: this.collection});
    this.$el.append(menu.render().el);
  }
};
