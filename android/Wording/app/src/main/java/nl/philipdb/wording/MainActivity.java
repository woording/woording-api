package nl.philipdb.wording;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.support.v7.widget.Toolbar;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.util.ArrayList;
import java.util.Arrays;

public class MainActivity extends AppCompatActivity {

    public static String username;

    private List[] mLists = new List[]{};
    private GetListsTask mGetListsTask;

    private Toolbar mToolbar;
    private RecyclerView mRecyclerView;
    private SwipeRefreshLayout mSwipeRefreshLayout;

    private static ListsViewAdapter mListsViewAdapter;

    protected static Context mContext;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Setup toolbar
        mToolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(mToolbar);

        // Setup RecyclerView
        mRecyclerView = (RecyclerView) findViewById(R.id.lists_view);
        // Setup LinearLayoutManager
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this);
        mRecyclerView.setLayoutManager(linearLayoutManager);
        // Setup RecyclerView Adapter
        mListsViewAdapter = new ListsViewAdapter(new ArrayList<>(Arrays.asList(mLists)));
        mRecyclerView.setAdapter(mListsViewAdapter);

        // Setup SwipeRefresLayout
        mSwipeRefreshLayout = (SwipeRefreshLayout) findViewById(R.id.swipe_refresh_layout);
        mSwipeRefreshLayout.setColorSchemeResources(R.color.accent);
        mSwipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                getLists();
                mSwipeRefreshLayout.setRefreshing(false);
            }
        });

        // TODO: Needs better logic
        if (NetworkCaller.mToken == null) {
            Intent loginIntent = new Intent(this, LoginActivity.class);
            startActivity(loginIntent);
        } else getLists();

//        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
//        StrictMode.setThreadPolicy(policy);
        mContext = this;
    }

    @Override
    protected void onStart() {
        super.onStart();
        if (NetworkCaller.mToken != null) getLists();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        // int id = item.getItemId();



        return super.onOptionsItemSelected(item);
    }

    public void getLists() {
        if (mGetListsTask != null) {
            return;
        }

        mGetListsTask = new GetListsTask();
        mGetListsTask.execute((Void) null);
    }

    public class GetListsTask extends AsyncTask<Void, Void, Boolean> {

        GetListsTask() {
        }

        @Override
        protected Boolean doInBackground(Void... params) {
            HttpURLConnection urlConnection = null;
            JSONObject response = null;

            try {
                // Initialize connection
                urlConnection = NetworkCaller.setupConnection("/" + username);
                // Add content
                JSONObject data = new JSONObject();
                data.put("token", NetworkCaller.mToken);
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

                    response = new JSONObject(json.toString());

                    inputStream.close();

                    // Handle the response
                    JSONArray jsonArray = response.getJSONArray("lists");
                    JSONObject listObject;
                    mLists = new List[jsonArray.length()];
                    for (int i = 0; i < jsonArray.length(); i ++) {
                        listObject = jsonArray.getJSONObject(i);
                        List tmp = new List(listObject.getString("listname"), listObject.getString("language_1_tag"),
                                listObject.getString("language_2_tag"), listObject.getString("shared_with"));
                        mLists[i] = tmp;
                    }
                }
            } catch (IOException e) {
                Log.d("IOException", "Something bad happened on the IO");
            } catch (JSONException e) {
                Log.d("JSONException", "The JSON fails");
            } finally {
                if (urlConnection != null) urlConnection.disconnect();
            }

            return response != null;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            mGetListsTask = null;

            if (success) {
                mListsViewAdapter.updateList(mLists);
            }
        }

        @Override
        protected void onCancelled() {
            mGetListsTask = null;
        }
    }
}
