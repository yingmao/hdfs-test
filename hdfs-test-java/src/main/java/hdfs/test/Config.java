package hdfs.test;

import org.apache.hadoop.conf.Configuration;

import java.io.IOException;
import java.util.Properties;

public class Config {

    private static Properties prop = new Properties();
    static {
        try {
            prop.load(Config.class.getResourceAsStream("/hdfs.properties"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String getHdfsUri(){
        return prop.getProperty("hdfs.uri");
    }


    public static Configuration getHdfsConfig(){
        Configuration conf = new Configuration();
        conf.set("fs.defaultFS",getHdfsUri());
        conf.set("dfs.client.use.datanode.hostname", "true");
        return conf;
    }

}
