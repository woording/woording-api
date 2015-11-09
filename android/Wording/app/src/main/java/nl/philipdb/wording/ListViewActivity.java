package nl.philipdb.wording;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

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

public class ListViewActivity extends AppCompatActivity {

    private GetListTask mGetListTask = null;

    private String mListName;
    private List mList;

    private ProgressBar mProgressBar;
    private LinearLayout mLinearLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list_view);

        // Setup toolbar
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        mProgressBar = (ProgressBar) findViewById(R.id.get_list_progress);
        mLinearLayout = (LinearLayout) findViewById(R.id.list_view_layout);

        // Load List from Intent
        mListName = getIntent().getStringExtra("listname");
        getList();

//        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
//        fab.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
//                        .setAction("Action", null).show();
//            }
//        });
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_list_view, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_practice) {
            // TODO: Create way to ask these parameters

            // Create and launch new intent
            Intent newIntent = new Intent(this, PracticeActivity.class);
            newIntent.putExtra("list", mList);
            newIntent.putExtra("askedLanguage", 1);
            newIntent.putExtra("caseSensitive", true);
            startActivity(newIntent);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    private void setWordsTable() {
        // Set title and languages
        getSupportActionBar().setTitle(mList.mName);
        ((TextView) findViewById(R.id.language_1)).setText(List.getLanguageName(mList.mLanguage1));
        ((TextView) findViewById(R.id.language_2)).setText(List.getLanguageName(mList.mLanguage2));

        // Set words
        TableLayout table = (TableLayout) findViewById(R.id.word_table);
        for (int i = 0; i < mList.getTotalWords(); i++) {
            TableRow tableRow = new TableRow(this);
            tableRow.setLayoutParams(new TableRow.LayoutParams(TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.WRAP_CONTENT, 1f));
            tableRow.setOrientation(LinearLayout.HORIZONTAL);

            TextView word1 = new TextView(this);
            word1.setLayoutParams(new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT, 1f));
            word1.setText(mList.mLanguage1Words.get(i));
            tableRow.addView(word1);

            TextView word2 = new TextView(this);
            word2.setLayoutParams(new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT, 1f));
            word2.setText(mList.mLanguage2Words.get(i));
            tableRow.addView(word2);

            table.addView(tableRow);
        }
    }

    public void getList() {
        if (mGetListTask != null) {
            return;
        }

        showProgress(true);
        mGetListTask = new GetListTask(mListName, MainActivity.username);
        mGetListTask.execute((Void) null);
    }

    public void showProgress(final boolean show) {
        // On Honeycomb MR2 we have the ViewPropertyAnimator APIs, which allow
        // for very easy animations. If available, use these APIs to fade-in
        // the progress spinner.
        int shortAnimTime = getResources().getInteger(android.R.integer.config_shortAnimTime);

        mLinearLayout.setVisibility(show ? View.GONE : View.VISIBLE);
        mLinearLayout.animate().setDuration(shortAnimTime).alpha(show ? 0 : 1).setListener(new AnimatorListenerAdapter() {
            @Override
            public void onAnimationEnd(Animator animation) {
                mLinearLayout.setVisibility(show ? View.GONE : View.VISIBLE);
            }
        });

        mProgressBar.setVisibility(show ? View.VISIBLE : View.GONE);
        mProgressBar.animate().setDuration(shortAnimTime).alpha(show ? 1 : 0).setListener(new AnimatorListenerAdapter() {
            @Override
            public void onAnimationEnd(Animator animation) {
                mProgressBar.setVisibility(show ? View.VISIBLE : View.GONE);
            }
        });
    }

    public class GetListTask extends AsyncTask<Void, Void, Boolean> {

        private final String mListName;
        private final String mUsername;

        GetListTask(String listName, String username) {
            mListName = listName;
            mUsername = username;
        }

        @Override
        protected Boolean doInBackground(Void... params) {
            HttpURLConnection urlConnection = null;
            JSONObject response = null;

            try {
                // Initialize connection
                urlConnection = NetworkCaller.setupConnection("/" + mUsername + "/" + mListName.replace(" ", "%20"));
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

                    mList = new List(response.getString("listname"), response.getString("language_1_tag"),
                            response.getString("language_2_tag"), response.getString("shared_with"));
                    JSONArray JSONWords = response.getJSONArray("words");
                    ArrayList<String> language1Words = new ArrayList<>();
                    ArrayList<String> language2Words = new ArrayList<>();
                    for (int i = 0; i < JSONWords.length(); i++) {
                        JSONObject object = JSONWords.getJSONObject(i);
                        language1Words.add(object.getString("language_1_text"));
                        language2Words.add(object.getString("language_2_text"));
                    }
                    mList.setWords(language1Words, language2Words);
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
            mGetListTask = null;
            showProgress(false);

            if (success) {
                setWordsTable();
            } else {
                finish();
            }
        }

        @Override
        protected void onCancelled() {
            mGetListTask = null;
            showProgress(false);
        }

    }

}
