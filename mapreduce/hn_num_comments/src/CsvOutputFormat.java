import java.io.DataOutputStream;
import java.io.IOException;

import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.OutputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.RecordWriter;

public class CsvOutputFormat<K, V> extends FileOutputFormat<K, V> {

    public class CsvRecordWriter<K, V> extends RecordWriter<K, V> {
        private DataOutputStream out;

        public CsvRecordWriter(DataOutputStream out) {
            this.out = out;
        }

        @Override
        public void write(K key, V value) throws IOException {
            try {
                out.writeBytes(key.toString() + "," + value.toString());
                out.writeBytes("\r\n");
            } catch (Exception ex) {
                out.close();
            }
        }

        @Override
        public void close(TaskAttemptContext context) throws IOException {
            out.close();
        }
    }

    @Override
    public RecordWriter<K, V> getRecordWriter(TaskAttemptContext context) 
        throws IOException, InterruptedException {
        // Get the output path of our file
        Path path = FileOutputFormat.getOutputPath(context);
        Path fullPath = new Path(path, "results.txt");
        // Create the file in the file system
        FileSystem fs = path.getFileSystem(context.getConfiguration());
        FSDataOutputStream fileOut = fs.create(fullPath, context);
        // Return the record write that will write to file
        return new CsvRecordWriter<K, V>(fileOut);
    }

}
