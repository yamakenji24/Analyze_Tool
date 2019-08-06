# coding: utf-8
require 'csv'
require 'time'

raised_data = CSV.read('./2018_raised.csv')
students = CSV.read('./studentlist.csv')
contests = CSV.read('./vrounded_contest.csv')

contests.each do |contest|
  base = Time.parse(contest[3])

  students.each do |student|
    each_csv = CSV.generate do |csv|
      csv << ['time_from_start', 'times_raised', 'time', 'mode']
      count = 0
      raised_data.each do |data|
        if(data[7] == student[0] && contest[10] == data[9])
          diff_from_start = (Time.parse(data[5]) - base)/60
          if (data[4] == '10')
            count += 1
          end
          each_csv = [
            diff_from_start, # 挙手時の経過時間
            count,   # 挙手回数
            data[5], # 時間
            data[4] # mode
          ]
          csv << each_csv
        end
      end
      puts(each_csv)
    end
    File.open('./'+contest[10]+'/'+student[0]+'.csv', 'w') do |file|
      file << each_csv
    end
  end

end
