package com.example.twitter;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.HttpStatus;

import java.io.IOException;

public class TwitterClient {
    private static final String BASE_URL = "https://api.twitter.com/2/tweets/search/recent?query=";

    public static void fetchTweets(String query) {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpGet request = new HttpGet(BASE_URL + query);
            request.setHeader("Authorization", "Bearer " + TwitterConfig.BEARER_TOKEN);

            try (CloseableHttpResponse response = httpClient.execute(request)) {
                int statusCode = response.getCode();

                if (statusCode == HttpStatus.SC_OK) {
                    HttpEntity entity = response.getEntity();
                    if (entity != null) {
                        String json = EntityUtils.toString(entity);
                        JsonObject jsonResponse = JsonParser.parseString(json).getAsJsonObject();
                        System.out.println("✅ Tweets fetched successfully:\n" + jsonResponse.toString());
                    } else {
                        System.out.println("⚠️ Empty response received.");
                    }
                } else {
                    System.err.println("❌ API request failed. HTTP Status Code: " + statusCode);
                }
            }
        } catch (IOException e) {
            System.err.println("❌ Error fetching tweets: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        fetchTweets("java");
    }
}
