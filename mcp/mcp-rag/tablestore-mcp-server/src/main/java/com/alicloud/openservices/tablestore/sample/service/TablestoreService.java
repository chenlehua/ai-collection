package com.alicloud.openservices.tablestore.sample.service;

import com.alicloud.openservices.tablestore.SyncClient;
import com.alicloud.openservices.tablestore.core.utils.ValueUtil;
import com.alicloud.openservices.tablestore.model.CapacityUnit;
import com.alicloud.openservices.tablestore.model.Column;
import com.alicloud.openservices.tablestore.model.ColumnType;
import com.alicloud.openservices.tablestore.model.ColumnValue;
import com.alicloud.openservices.tablestore.model.CreateTableRequest;
import com.alicloud.openservices.tablestore.model.ListTableResponse;
import com.alicloud.openservices.tablestore.model.PrimaryKey;
import com.alicloud.openservices.tablestore.model.PrimaryKeyBuilder;
import com.alicloud.openservices.tablestore.model.PrimaryKeySchema;
import com.alicloud.openservices.tablestore.model.PrimaryKeyType;
import com.alicloud.openservices.tablestore.model.PrimaryKeyValue;
import com.alicloud.openservices.tablestore.model.PutRowRequest;
import com.alicloud.openservices.tablestore.model.ReservedThroughput;
import com.alicloud.openservices.tablestore.model.Row;
import com.alicloud.openservices.tablestore.model.RowPutChange;
import com.alicloud.openservices.tablestore.model.TableMeta;
import com.alicloud.openservices.tablestore.model.TableOptions;
import com.alicloud.openservices.tablestore.model.search.CreateSearchIndexRequest;
import com.alicloud.openservices.tablestore.model.search.DescribeSearchIndexRequest;
import com.alicloud.openservices.tablestore.model.search.DescribeSearchIndexResponse;
import com.alicloud.openservices.tablestore.model.search.FieldSchema;
import com.alicloud.openservices.tablestore.model.search.FieldType;
import com.alicloud.openservices.tablestore.model.search.IndexSchema;
import com.alicloud.openservices.tablestore.model.search.ListSearchIndexRequest;
import com.alicloud.openservices.tablestore.model.search.ListSearchIndexResponse;
import com.alicloud.openservices.tablestore.model.search.SearchHit;
import com.alicloud.openservices.tablestore.model.search.SearchIndexInfo;
import com.alicloud.openservices.tablestore.model.search.SearchQuery;
import com.alicloud.openservices.tablestore.model.search.SearchRequest;
import com.alicloud.openservices.tablestore.model.search.SearchResponse;
import com.alicloud.openservices.tablestore.model.search.query.QueryBuilders;
import com.alicloud.openservices.tablestore.model.search.sort.ScoreSort;
import com.alicloud.openservices.tablestore.model.search.sort.Sort;
import com.alicloud.openservices.tablestore.model.search.vector.VectorDataType;
import com.alicloud.openservices.tablestore.model.search.vector.VectorMetricType;
import com.alicloud.openservices.tablestore.model.search.vector.VectorOptions;
import com.alicloud.openservices.tablestore.sample.config.EnvironmentSettings;
import com.alicloud.openservices.tablestore.sample.model.FAQContent;
import com.alicloud.openservices.tablestore.sample.model.KnowledgeContent;
import com.alicloud.openservices.tablestore.sample.model.SearchFAQQuery;
import com.alicloud.openservices.tablestore.sample.model.SearchKnowledgeQuery;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.io.Closeable;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;


@Slf4j
@Component
public class TablestoreService implements Closeable {

    private final SyncClient client;
    private final EmbeddingService embeddingService;
    private final String knowledgeStore;
    private final String knowledgeIndex;
    private final String faqStore;
    private final String faqIndex;
    private final String pkName;
    private final String textField;
    private final String embeddingField;
    private final int vectorDimension;
    private final List<FieldSchema> metadataSchemaList;
    private final String faqAnswerFieldName;

    public TablestoreService(EmbeddingService embeddingService) {
        this.embeddingService = embeddingService;
        String instanceName = EnvironmentSettings.getTablestoreInstanceName();
        String endpoint = EnvironmentSettings.getTablestoreEndpoint();
        String accessKeyId = EnvironmentSettings.getTablestoreAccessKeyId();
        String accessKeySecret = EnvironmentSettings.getTablestoreAccessKeySecret();
        this.client = new SyncClient(endpoint, accessKeyId, accessKeySecret, instanceName);
        this.knowledgeStore = EnvironmentSettings.getKnowledgeTableName();
        this.knowledgeIndex = EnvironmentSettings.getKnowledgeIndexName();
        this.faqStore = EnvironmentSettings.getFAQTableName();
        this.faqIndex = EnvironmentSettings.getFAQIndexName();
        this.pkName = EnvironmentSettings.getTablePkName();
        this.textField = EnvironmentSettings.getTextFieldName();
        this.embeddingField = EnvironmentSettings.getVectorFieldName();
        this.vectorDimension = EnvironmentSettings.getVectorDimension();
        this.faqAnswerFieldName = EnvironmentSettings.getFAQAnswerFieldName();
        List<FieldSchema> tmpMetaList = new ArrayList<>();
        tmpMetaList.add(new FieldSchema(textField, FieldType.TEXT).setIndex(true).setAnalyzer(FieldSchema.Analyzer.MaxWord));
        tmpMetaList.add(new FieldSchema(embeddingField, FieldType.VECTOR).setIndex(true).setVectorOptions(new VectorOptions(VectorDataType.FLOAT_32, vectorDimension, VectorMetricType.COSINE)));
        this.metadataSchemaList = tmpMetaList;
        init();
    }

    public void storeKnowledge(KnowledgeContent entry) {
        String id = UUID.randomUUID().toString();
        addKnowledge(id, entry);
    }

    public List<KnowledgeContent> searchKnowledge(SearchKnowledgeQuery request) {
        String query = request.getQuery();
        int size = request.getSize();
        log.info("search knowledge query:[{}], size:{}", query, size);
        float[] embedQuery = embeddingService.embed(query);

        SearchQuery searchQuery = SearchQuery.newBuilder()
                .query(QueryBuilders.bool()
                        .should(QueryBuilders.knnVector(embeddingField, Math.min(1000, size + 100), embedQuery))
                        //.should(QueryBuilders.match(textField, query)) // only vector search, later can try mix search
                )
                .getTotalCount(false)
                .limit(size)
                .offset(0)
                .sort(new Sort(Collections.singletonList(new ScoreSort())))
                .build();
        SearchRequest searchRequest = SearchRequest.newBuilder()
                .tableName(knowledgeStore)
                .indexName(knowledgeIndex)
                .searchQuery(searchQuery)
                .returnAllColumns(true)
                .build();
        SearchResponse response = client.search(searchRequest);
        log.info("search knowledge requestId:{}", response.getRequestId());
        return searchResponseToKnowledgeContent(response);
    }

    public void storeFAQ(FAQContent entry) {
        String id = UUID.randomUUID().toString();
        addFAQ(id, entry);
    }

    public List<FAQContent> searchFAQ(SearchFAQQuery request) {
        String query = request.getQuery();
        int size = request.getSize();
        log.info("search faq:[{}], size:{}", query, size);
        float[] embedQuery = embeddingService.embed(query);

        SearchQuery searchQuery = SearchQuery.newBuilder()
                .query(QueryBuilders.bool()
                        .should(QueryBuilders.knnVector(embeddingField, Math.min(1000, size + 100), embedQuery))
                        .should(QueryBuilders.match(textField, query))
                )
                .getTotalCount(false)
                .limit(size)
                .offset(0)
                .sort(new Sort(Collections.singletonList(new ScoreSort())))
                .build();
        SearchRequest searchRequest = SearchRequest.newBuilder()
                .tableName(faqStore)
                .indexName(faqIndex)
                .searchQuery(searchQuery)
                .returnAllColumns(true)
                .build();
        SearchResponse response = client.search(searchRequest);
        log.info("search requestId:{}", response.getRequestId());
        return searchResponseToFAQContent(response);
    }


    private List<KnowledgeContent> searchResponseToKnowledgeContent(SearchResponse response) {
        List<SearchHit> searchHits = response.getSearchHits();
        List<KnowledgeContent> matches = new ArrayList<>(searchHits.size());
        for (SearchHit hit : searchHits) {
            Double score = hit.getScore();
            // 如果对分数有要求，可以这里进行限制.
            Row row = hit.getRow();

            String text = "";
            if (row.getLatestColumn(textField) != null) {
                text = row.getLatestColumn(textField).getValue().asString();
            }

            Map<String, Object> metaData = rowToMetadata(row);
            matches.add(new KnowledgeContent(text, metaData));
        }
        return matches;
    }

    private List<FAQContent> searchResponseToFAQContent(SearchResponse response) {
        List<SearchHit> searchHits = response.getSearchHits();
        List<FAQContent> matches = new ArrayList<>(searchHits.size());
        for (SearchHit hit : searchHits) {
            Double score = hit.getScore();
            // 如果对分数有要求，可以这里进行限制.
            Row row = hit.getRow();

            String text = "";
            if (row.getLatestColumn(textField) != null) {
                text = row.getLatestColumn(textField).getValue().asString();
            }

            String answer = row.getLatestColumn(faqAnswerFieldName).getValue().asString();

            matches.add(new FAQContent(text, answer));
        }
        return matches;
    }

    private Map<String, Object> rowToMetadata(Row row) {
        Map<String, Object> metadata = new HashMap<>();
        for (Column column : row.getColumns()) {
            if (column.getName().equals(embeddingField)) {
                continue;
            }
            if (column.getName().equals(textField)) {
                continue;
            }
            ColumnType columnType = column.getValue().getType();
            switch (columnType) {
                case STRING:
                    metadata.put(column.getName(), column.getValue().asString());
                    break;
                case INTEGER:
                    metadata.put(column.getName(), column.getValue().asLong());
                    break;
                case DOUBLE:
                    metadata.put(column.getName(), column.getValue().asDouble());
                    break;
                default:
                    log.warn("unsupported columnType:{}, key:{}, value:{}", columnType, column.getName(), column.getValue());
            }
        }
        return metadata;
    }

    private void init() {
        createTableIfNotExist(knowledgeStore);
        createSearchIndexIfNotExist(knowledgeStore, knowledgeIndex);

        createTableIfNotExist(faqStore);
        createSearchIndexIfNotExist(faqStore, faqIndex);

        checkEmbeddingDimension();
        checkSchemaDimension(knowledgeStore, knowledgeIndex);
        checkSchemaDimension(faqStore, faqIndex);
    }

    private boolean tableExists(String tableName) {
        ListTableResponse listTableResponse = client.listTable();
        return listTableResponse.getTableNames().contains(tableName);
    }

    private void createTableIfNotExist(String tableName) {
        if (tableExists(tableName)) {
            log.info("table:{} already exists", tableName);
            return;
        }
        TableMeta tableMeta = new TableMeta(tableName);
        tableMeta.addPrimaryKeyColumn(new PrimaryKeySchema(pkName, PrimaryKeyType.STRING));
        TableOptions tableOptions = new TableOptions(-1, 1);
        CreateTableRequest request = new CreateTableRequest(tableMeta, tableOptions);
        request.setReservedThroughput(new ReservedThroughput(new CapacityUnit(0, 0)));
        client.createTable(request);
        log.info("create table:{}", tableName);
    }

    private void createSearchIndexIfNotExist(String tableName, String indexName) {
        if (searchindexExists(tableName, indexName)) {
            log.info("index:{} already exists", indexName);
            return;
        }
        CreateSearchIndexRequest request = new CreateSearchIndexRequest();
        request.setTableName(tableName);
        request.setIndexName(indexName);
        IndexSchema indexSchema = new IndexSchema();
        indexSchema.setFieldSchemas(metadataSchemaList);
        request.setIndexSchema(indexSchema);
        client.createSearchIndex(request);
        log.info("create index:{}", indexName);
    }

    private boolean searchindexExists(String tableName, String indexName) {
        List<SearchIndexInfo> searchIndexInfos = listSearchIndex(tableName);
        for (SearchIndexInfo indexInfo : searchIndexInfos) {
            if (indexInfo.getIndexName().equals(indexName)) {
                return true;
            }
        }
        return false;
    }

    private List<SearchIndexInfo> listSearchIndex(String tableName) {
        ListSearchIndexRequest request = new ListSearchIndexRequest();
        request.setTableName(tableName);
        ListSearchIndexResponse listSearchIndexResponse = client.listSearchIndex(request);
        return listSearchIndexResponse.getIndexInfos();
    }

    private void checkEmbeddingDimension() {
        float[] embed = embeddingService.embed("test");
        if (embed.length != vectorDimension) {
            throw new IllegalArgumentException(String.format("the embeddingService's embedding dimension is:%d, but the config vector dimension is:%d", embed.length, vectorDimension));
        }
    }

    private void checkSchemaDimension(String tableName, String indexName) {
        DescribeSearchIndexRequest request = new DescribeSearchIndexRequest();
        request.setTableName(tableName);
        request.setIndexName(indexName);
        DescribeSearchIndexResponse response = client.describeSearchIndex(request);
        for (FieldSchema schema : response.getSchema().getFieldSchemas()) {
            if (schema.getFieldName().equals(embeddingField)) {
                VectorOptions vectorOptions = schema.getVectorOptions();
                if (vectorOptions == null) {
                    throw new IllegalArgumentException(String.format("the vector field:%s does not have vector options", embeddingField));
                }
                if (vectorOptions.getDimension() != vectorDimension) {
                    throw new IllegalArgumentException(String.format("the vector field:%s has dimension:%d, but the embedding dimension is:%d", embeddingField, vectorOptions.getDimension(), vectorDimension));
                }
            }
        }
    }

    private void addKnowledge(String id, KnowledgeContent entry) {
        PrimaryKeyBuilder primaryKeyBuilder = PrimaryKeyBuilder.createPrimaryKeyBuilder();
        primaryKeyBuilder.addPrimaryKeyColumn(this.pkName, PrimaryKeyValue.fromString(id));
        PrimaryKey primaryKey = primaryKeyBuilder.build();
        RowPutChange rowPutChange = new RowPutChange(this.knowledgeStore, primaryKey);
        float[] embed = embeddingService.embed(entry.getContent());
        String embeddingString = embeddingToString(embed);
        rowPutChange.addColumn(new Column(this.embeddingField, ColumnValue.fromString(embeddingString)));
        String text = entry.getContent();
        if (text != null) {
            rowPutChange.addColumn(new Column(this.textField, ColumnValue.fromString(text)));
        }
        Map<String, Object> map = entry.getMetaData();
        if (map != null) {
            for (Map.Entry<String, Object> e : map.entrySet()) {
                String key = e.getKey();
                Object value = e.getValue();
                if (this.textField.equals(key)) {
                    throw new IllegalArgumentException(String.format("there is a metadata(%s,%s) that is consistent with the name of the text field:%s", key, value, this.textField));
                }
                if (this.embeddingField.equals(key)) {
                    throw new IllegalArgumentException(String.format("there is a metadata(%s,%s) that is consistent with the name of the vector field:%s", key, value, this.embeddingField));
                }
                if (value instanceof Float) {
                    rowPutChange.addColumn(new Column(key, ColumnValue.fromDouble((Float) value)));
                } else if (value instanceof UUID) {
                    rowPutChange.addColumn(new Column(key, ColumnValue.fromString(((UUID) value).toString())));
                } else {
                    rowPutChange.addColumn(new Column(key, ValueUtil.toColumnValue(value)));
                }
            }
        }
        try {
            log.info("store entry id:{}, content:{}, metaData:{}, embedding:{}", id, entry.getContent(), entry.getMetaData(), maxLogOrNull(embeddingString));
            client.putRow(new PutRowRequest(rowPutChange));
        } catch (Exception e) {
            throw new RuntimeException(String.format("store entry failed, id:%s, content:%s, metaData:%s, embedding:%s", id, entry.getContent(), entry.getMetaData(), maxLogOrNull(embeddingString)), e);
        }
    }

    private void addFAQ(String id, FAQContent entry) {
        PrimaryKeyBuilder primaryKeyBuilder = PrimaryKeyBuilder.createPrimaryKeyBuilder();
        primaryKeyBuilder.addPrimaryKeyColumn(this.pkName, PrimaryKeyValue.fromString(id));
        PrimaryKey primaryKey = primaryKeyBuilder.build();
        RowPutChange rowPutChange = new RowPutChange(this.faqStore, primaryKey);
        float[] embed = embeddingService.embed(entry.getQuestion());
        String embeddingString = embeddingToString(embed);
        rowPutChange.addColumn(new Column(this.embeddingField, ColumnValue.fromString(embeddingString)));
        String text = entry.getQuestion();
        if (text != null) {
            rowPutChange.addColumn(new Column(this.textField, ColumnValue.fromString(text)));
        }
        rowPutChange.addColumn(new Column(this.faqAnswerFieldName, ColumnValue.fromString(entry.getAnswer())));
        try {
            log.info("store entry id:{}, question:{}, answer:{}, embedding:{}", id, entry.getQuestion(), entry.getAnswer(), maxLogOrNull(embeddingString));
            client.putRow(new PutRowRequest(rowPutChange));
        } catch (Exception e) {
            throw new RuntimeException(String.format("store entry failed, id:%s, question:%s, embedding:%s", id, entry.getQuestion(), maxLogOrNull(embeddingString)), e);
        }
    }

    private static final ObjectMapper JSON_MAPPER = new ObjectMapper();

    private static float[] parseEmbeddingString(String embeddingString) {
        return JSON_MAPPER.convertValue(embeddingString, float[].class);
    }

    private static String embeddingToString(float[] embedding) {
        try {
            return JSON_MAPPER.writeValueAsString(embedding);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(String.format("failed to write embedding to string, embedding:%s", Arrays.toString(embedding)), e);
        }
    }

    private static String maxLogOrNull(String str) {
        if (str == null) {
            return null;
        }
        int max = 200;
        if (str.length() <= max) {
            return str;
        }
        return str.substring(0, max) + "......";
    }

    @Override
    @PreDestroy
    public void close() throws IOException {
        log.info("closing tablestore client");
        if (client != null) {
            try {
                client.shutdown();
            } catch (Exception e) {
                log.error("failed to shutdown tablestore client", e);
            }
        }
    }
}
