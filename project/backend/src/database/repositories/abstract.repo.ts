import { Document, FilterQuery, Types, UpdateQuery } from 'mongoose';

const restrictedFields: string = '-password -tokenUpdateLogin -token' as string;

interface Group {
  _id: string;
  count: number;
}

interface Result {
  groups: Group[];
  total: number;
}

/**
 * Generic Repositoria Interface.
 * @template T type model repository.
 */
export interface IRepository<T> {
  /**
   * CreateOne(payload) create one database register
   * @param {*} payload as CreateModelDto
   * @returns {Promise<any>}
   *
   * @example
   * const payload = { name: "Arise Technology" } as CreateModelDto
   * this.repository.createOne(payload);
   */
  createOne(payload: any): Promise<any>;

  /**
   * createMany(payload) Create many database registers
   * @param {*} payload
   * @returns {Promise<any>}
   *
   * @example
   * const payload = [{ name: "Arise Technology" }, { name: "Soil App" }] as CreateModelDto[]
   * this.repository.createMany(payload);
   */
  createMany(payload: any): Promise<any>;

  /**
   * updateOne(_id, payload, ignoreValidation?) update one register
   * @param {(string | Types.ObjectId)} _id mongo ID
   * @param {UpdateQuery<T>} payload data to update
   * @param {?boolean} [ignoreValidation] ignore all schema validations
   * @returns {Promise<any | null>}
   *
   * @example
   * const payload = { name: "Arise Technology Updated" } as UpdateModelDto
   * this.repository.updateOne(_id , payload, true);
   */
  updateOne(
    _id: string | Types.ObjectId,
    payload: UpdateQuery<T>,
    ignoreValidation?: boolean
  ): Promise<any | null>;

  /**
   * updateAny(query, payload) update any register. More flexible updater
   * @param {(string | Types.ObjectId)} query mongoose query
   * @param {UpdateQuery<T>} payload data to update
   * @returns {Promise<any | null>}
   *
   * @example
   * const query = { email: "arise@email.com" }
   * const payload = {name: "Arise Technology"}
   * this.repository.updateOne(_id , payload);
   */
  updateAny(query: any, payload: UpdateQuery<T>): Promise<any | null>;

  /**
   * updateMany(filter, payload) update many registers
   * @param {(string | Types.ObjectId)} filter mongoose filter
   * @param {UpdateQuery<T>} payload data to update
   * @returns {Promise<any | null>}
   *
   * @example
   * const query = ["63c051f9d08f86668030b16c", "63c072b5d08f86668030b17d"]
   * const payload = {name: "Arise Technology"}
   * this.repository.updateMany(query , payload);
   */
  updateMany(filter: any, payload: UpdateQuery<T>): Promise<any | null>;

  /**
   * find(filter, page: string, pageSize: string, populateFields?, includeFields?, isDeleted?, match?, populateCascate?)
   * does a filter on the IModel type and returns the records found
   * @param {FilterQuery<T>} filter mongoose  FilterQuery<IModel>
   * @param {number} [page] page number
   * @param {?number} [pageSize] page length
   * @param {?{ [key: string]: string }} [populateFields] make populate fields
   * @param {?{ [key: string]: string }} [populateMatchs] { [key: string]: any } make match populate field
   * @param {?{ [key: string]: string }} [populateCascate] { [key: string]: any } make match populate cascate
   * @param {?string[]} [includeFields] include sensitive fields as: passwords and tokens
   * @param {?boolean} [isDeleted] [true]: return deleted data, [undefined]: return active data, [false]: return active + deleted
   * @returns {Promise<T[]>}
   *
   * @example
   * const filtered = { name: "Arise Technology" } as FilterQuery<IModel>
   * const populateFields = { model: 'model' }
   * const match = { field: 'field' }
   * const populateCascate = {
   * 'produto': { model: 'Produto',
   *  populate: { path: 'especificacoes', model: 'Especificacoes' } } }
   *
   * this.repository.find(
   *     filtered,
   *     "1",
   *     "10",
   *     populateFields,
   *     populateMatch,
   *     populateCascate
   *     ['password'],
   *     true,
   *    );
   */
  find(
    filter: FilterQuery<T>,
    page?: number | 1,
    pageSize?: number,
    populateFields?: { [key: string]: string },
    populateMatchs?: { [key: string]: { model: string; match?: { [key: string]: any } } },
    populateCascate?: { [key: string]: { model: string; populate?: { model: string; path: string } } },
    includeFields?: string[],
    isDeleted?: boolean
  ): Promise<any[]>;

  /**
   * deleteOne(_id) make a softDelete for one register, changing schema status from isDeleted=false to isDeleted=true
   * @param {(string | Types.ObjectId)} _id mongoose _id
   * @returns {Promise<any>}
   *
   * @example
   * const _id = "63c051f9d08f86668030b16c"
   * this.repository.deleteOne(_id);
   */
  deleteOne(_id: string | Types.ObjectId, fieldsToClean: object): Promise<any>;

  /**
   * deleteOne(_id) make a softDelete for many registers, changing schema status from isDeleted=false to isDeleted=true
   * @param {(string | Types.ObjectId)} filter mongoose ids
   * @returns {Promise<any>}
   *
   * @example
   * const filter = { user: userId }
   * this.repository.deleteOne(filter);
   */
  deleteMany(filter: FilterQuery<T>): Promise<any>;

  /**
   * aggregation(match, groups, project) aggregate method to get statistics data
   * @param {Record<string, any>} match filter query
   * @param {Record<string, any>[]} groups to group the records and get statistical data
   * @param {?Record<string, any>} [project] choose the data to be returned
   * @returns {Promise<Result>}
   *
   * @example
   * const groups = [
   *   {
   *     $group: {
   *       sum: { $sum: '$totalPrice' },
   *     },
   *   },
   * ];
   *
   * const match = {
   *       consultant: new Types.ObjectId(_id),
   *     }
   *
   * this.repository.aggregation(match, groups);
   */ aggregation(
    match: Record<string, any>,
    groups: Record<string, any>[],
    project?: Record<string, any>
  ): Promise<Result>;
}

/**
 * Description placeholder
 * @date 14/03/2023 - 10:15:39
 *
 * @export
 * @class BaseRepository
 * @typedef {BaseRepository}
 * @template T
 * @implements {IRepository<T>}
 */
export class BaseRepository<T extends Document> implements IRepository<T> {
  private model: any;

  constructor(model: any) {
    this.model = model;
  }

  async createOne(payload: any): Promise<T> {
    const doc = await this.model.create(payload);
    return await this.model.findOne({ _id: doc._id }).select(restrictedFields).exec();
  }

  async createMany(payload: any): Promise<T> {
    return await this.model.insertMany(payload);
  }

  async updateOne(
    _id: string | Types.ObjectId,
    payload: UpdateQuery<T>,
    ignoreValidation?: boolean | false
  ): Promise<T> {
    if (ignoreValidation) {
      const updated = await this.model.findOneAndUpdate({ _id: _id }, payload).select(restrictedFields);
      return updated;
    } else {
      const updated = await this.model.findOneAndUpdate(
        { _id: _id },
        {
          ...payload,
        },
        {
          new: true,
        }
      );

      return updated;
    }
  }

  async updateMany(filter: FilterQuery<T>, payload: UpdateQuery<T>): Promise<T[]> {
    await this.model.updateMany(filter, payload);
    return this.model.find(filter);
  }

  async updateAny(query: any, payload: UpdateQuery<T>): Promise<T> {
    const updated = await this.model
      .findOneAndUpdate(
        query,
        {
          ...payload,
        },
        {
          new: true,
        }
      )
      .select(restrictedFields);

    return updated;
  }

  async find(
    filter: FilterQuery<T>,
    page?: number | 1,
    pageSize?: number,
    populateFields?: { [key: string]: string },
    populateMatchs?: { [key: string]: { model: string; match?: { [key: string]: any } } },
    populateCascate?: { [key: string]: { model: string; populate?: { model: string; path: string } } },
    includeFields?: string[],
    isDeleted?: boolean
  ): Promise<T[]> {
    const skip = (Number(page) - 1) * (Number(pageSize) || 0);

    const query = this.model
      .find(filter)
      .sort({ isDeleted: 1, createdAt: -1 })
      .skip(skip)
      .limit(Number(pageSize) || 0)
      .select(includeFields?.join(' '));

    if (populateMatchs) {
      const populateQuery = Object.entries(populateMatchs).map(([field, { model, match }]) => ({
        path: field,
        model,
        match,
        options: { strictPopulate: false },
      }));
      query.populate(populateQuery);
    } else if (populateFields) {
      const populateQuery = Object.entries(populateFields).map(([field, model]) => ({
        path: field,
        model,
        options: { strictPopulate: false },
      }));
      query.populate(populateQuery);
    } else if (populateCascate) {
      const populateQuery = Object.entries(populateCascate).map(([field, { model, populate }]) => ({
        path: field,
        populate: populate
          ? { path: populate.path, model: populate.model, options: { strictPopulate: false } }
          : undefined,
        model,
        options: { strictPopulate: false },
      }));
      query.populate(populateQuery);
    }

    if (typeof isDeleted === 'boolean') {
      query.where('isDeleted').equals(isDeleted);
    }

    return query.exec();
  }

  async deleteOne(_id: string | Types.ObjectId, fieldsToClean: object) {
    const deleted = await this.model.updateOne(
      { _id: _id },
      {
        ...fieldsToClean,
        isDeleted: true,
      }
    );
    return deleted;
  }

  async deleteMany(filter: FilterQuery<T>) {
    return await this.model.updateMany(filter, { isDeleted: true });
  }

  async aggregation(
    match: Record<string, any>,
    groups: Record<string, any>[],
    project?: Record<string, any>
  ) {
    const aggregation = [{ $match: match }, ...groups];
    if (project) {
      aggregation.push({ $project: project });
    }

    return await this.model.aggregate(aggregation);
  }
}
