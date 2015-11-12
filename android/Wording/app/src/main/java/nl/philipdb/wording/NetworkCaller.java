/*
 * Wording is a project by PhiliPdB
 *
 * Copyright (c) 2015.
 */

package nl.philipdb.wording;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

public class NetworkCaller {
    public static final String API_LOCATION = "http://api-wording.rhcloud.com";
    public static String mToken = null;

    public static HttpURLConnection setupConnection(String location) throws IOException {
        // Setup connection
        URL url = new URL(API_LOCATION + location);
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        urlConnection.setReadTimeout(15000);
        urlConnection.setConnectTimeout(15000);
        urlConnection.setRequestMethod("POST");
        urlConnection.setDoInput(true);
        urlConnection.setDoOutput(true);
        urlConnection.setUseCaches(true);
        urlConnection.setInstanceFollowRedirects(false);
        // Set the content-type as json --> Important
        urlConnection.setRequestProperty("Content-Type", "application/json;charset=utf-8");

        return urlConnection;
    }

    public static void deleteList(List list) throws  IOException {
        HttpURLConnection urlConnection = setupConnection("/deleteList");
    }

}
