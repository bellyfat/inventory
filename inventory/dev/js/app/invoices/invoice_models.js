/*
 * Invoice models
 *
 * js/models/invoice_models.js
 */

"use strict";


// Invoices
class InvoicesModel extends Backbone.Model {
  get defaults() {
    return {
      public_id: '',
      project: null,
      currency: null,
      supplier: null,
      invoices_number: '',
      invoice_date: '',
      credit: 0,
      shipping: 0,
      other: 0,
      tax: 0,
      notes: '',
      creator: '',
      created: '',
      updater: '',
      updated: '',
      href: ''
    };
  }

  get mutators() {
    return {
      invoice_items: {
        set(key, value, options, set) {
          var invoice_items = new InvoiceItemsCollection();
          set(key, invoice_items, options);

          _.forEach(value, function(value, key) {
            invoice_items.add(value);
          });
        }
      }
    };
  }

  url() {
    return this.get('href');
  }

  constructor(options) {
    super(options);
  }
};


class InvoicesMetaModel extends Backbone.Model {
  get defaults() {
    return {
      project_public_id: '',
      count: 0,
      next: null,
      previous: null,
      options: {}
    };
  }

  constructor(options) {
    super(options);
  }
};


class InvoicesCollection extends Backbone.Collection {
  get name() { return "InvoicesModel"; }
  get model() { return InvoicesModel; }

  constructor(options) {
    super(options);
  }

  parse(response, options) {
    let models = response.results;

    if(response.count > 0) {
      let project_public_id = models[0].project_public_id,
          invoicesMeta = new InvoicesMetaModel({
            project_public_id: project_public_id,
            count: response.count,
            next: response.next,
            previous: response.previous
          });
      App.models.invoicesMeta = invoicesMeta;
    }

    return models;
  }
};


// InvoiceItems
class InvoiceItemsModel extends Backbone.Model {
  get defaults() {
    return {
      invoice: '',
      invoice_public_id: '',
      item_number: '',
      description: '',
      quantity: 0,
      unit_price: '',
      process: true,
      item: '',
      href: ''
    };
  }

  url() {
    return this.get('href');
  }

  constructor(options) {
    super(options);
  }
};


class InvoiceItemsMetaModel extends Backbone.Model {
  get defaults() {
    return {
      invoice_public_id: '',
      count: 0,
      next: null,
      previous: null,
      options: {}
    };
  }

  constructor(options) {
    super(options);
  }
};


class InvoiceItemsCollection extends Backbone.Collection {
  get name() { return "InvoiceItemsModel"; }
  get model() { return InvoiceItemsModel; }

  constructor(options) {
    super(options);
  }
};


// Items
class ItemsModel extends Backbone.Model {
  get defaults() {
    return {
      public_id: '',
      project: null,
      sku: '',
      item_number: '',
      item_number_mfg: '',
      manufacturer: null,
      description: '',
      quantity: 0,
      categories: [],
      location_codes: [],
      shared_projects: [],
      purge: false,
      active: false,
      creator: '',
      created: '',
      updater: '',
      updated: '',
      href: ''
    };
  }

  url() {
    return this.get('href');
  }

  constructor(options) {
    super(options);
  }
};


class ItemsMetaModel extends Backbone.Model {
  get defaults() {
    return {
      count: 0,
      next: null,
      previous: null,
      options: {}
    };
  }

  constructor(options) {
    super(options);
  }
};


class ItemsCollection extends Backbone.Collection {
  get name() { return "ItemsModel"; }
  get model() { return ItemsModel; }

  constructor(options) {
    super(options);
  }

  parse(response, options) {
    let models = response.results;

    if(response.count > 0) {
      let project_public_id = models[0].project_public_id,
          itemsMeta = new ItemsMetaModel({
            project_public_id: project_public_id,
            count: response.count,
            next: response.next,
            previous: response.previous
          });

      App.models.itemsMeta = itemsMeta;
    }

    return models;
  }
};
