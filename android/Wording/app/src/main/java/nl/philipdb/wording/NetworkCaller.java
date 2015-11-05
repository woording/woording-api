package nl.philipdb.wording;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class NetworkCaller {
    public static final String API_LOCATION = "http://api-wording.rhcloud.com";
    public static String mToken;

    public static HttpURLConnection setupConnection(String location) throws IOException {
        HttpURLConnection urlConnection = null;
        // Setup connection
        URL url = new URL(API_LOCATION + location);
        urlConnection = (HttpURLConnection) url.openConnection();
        urlConnection.setReadTimeout(15000);
        urlConnection.setConnectTimeout(15000);
        urlConnection.setRequestMethod("POST");
        urlConnection.setDoInput(true);
        urlConnection.setDoOutput(true);
        urlConnection.setUseCaches(false);
        urlConnection.setInstanceFollowRedirects(false);
        // Set the content-type as json --> Important
        urlConnection.setRequestProperty("Content-Type", "application/json;charset=utf-8");

        return urlConnection;
    }

    public static List[] getLists(String username) throws Exception {
        List[] lists = null;

        // Initialize connection
        HttpURLConnection urlConnection = setupConnection("/" + username);
        // Add content
        JSONObject data = new JSONObject();
        data.put("token", mToken);
        // And send the data
        OutputStream output = urlConnection.getOutputStream();
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(output, "UTF-8"));
        writer.write(data.toString());
        writer.flush();
        writer.close();
        output.close();
        // And connect
        urlConnection.connect();

        // Check for the response from the server
        if (urlConnection.getResponseCode() == HttpURLConnection.HTTP_OK) {
            InputStream inputStream = urlConnection.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
            StringBuilder json = new StringBuilder();
            String inputLine = "";

            while ((inputLine = bufferedReader.readLine()) != null) {
                json.append(inputLine);
            }

            JSONObject response = new JSONObject(json.toString());

            inputStream.close();

            // Handle the response
            JSONArray jsonArray = response.getJSONArray("lists");
            JSONObject listObject;
            lists = new List[jsonArray.length()];
            for (int i = 0; i < jsonArray.length(); i ++) {
                listObject = jsonArray.getJSONObject(i);
                List tmp = new List(listObject.getString("listname"), listObject.getString("language_1_tag"),
                        listObject.getString("language_2_tag"), listObject.getString("shared_with"));
                lists[i] = tmp;
            }
            // TODO: Create function that sorts the lists
        }

        return lists;
    }

    public static void deleteList(List list) throws  IOException {
        HttpURLConnection urlConnection = setupConnection("/deleteList");
    }

}
