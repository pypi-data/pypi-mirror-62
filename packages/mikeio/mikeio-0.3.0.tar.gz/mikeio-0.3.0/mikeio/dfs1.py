import numpy as np
from datetime import datetime
import System
from System import Array
from DHI.Generic.MikeZero import eumUnit, eumQuantity
from DHI.Generic.MikeZero.DFS import (
    DfsFileFactory,
    DfsFactory,
    DfsSimpleType,
    DataValueType,
)
from DHI.Generic.MikeZero.DFS.dfs123 import Dfs1Builder

from .dutil import to_numpy, Dataset, find_item
from .eum import TimeStep
from .helpers import safe_length


class Dfs1:
    def read(self, filename, item_numbers=None, item_names=None):
        """Read data from the dfs1 file

        Usage:
            read(filename, item_numbers=None, item_names=None)
        filename
            full path to the dfs1 file.
        item_numbers
            read only the item_numbers in the array specified (0 base)
        item_names
            read only the items in the array specified, (takes precedence over item_numbers)

        Return:
            Dataset(data, time, names)
            where data[nt,x]
        """

        # NOTE. Item numbers are base 0 (everything else in the dfs is base 0)

        # Open the dfs file for reading
        dfs = DfsFileFactory.DfsGenericOpen(filename)

        if item_names is not None:
            item_numbers = find_item(dfs, item_names)

        if item_numbers is None:
            n_items = safe_length(dfs.ItemInfo)
            item_numbers = list(range(n_items))

        # Determine the size of the grid
        axis = dfs.ItemInfo[0].SpatialAxis

        xNum = axis.XCount
        nt = dfs.FileInfo.TimeAxis.NumberOfTimeSteps
        if nt == 0:
            raise Warning("Static dfs1 files (with no time steps) are not supported.")
            nt = 1
        deleteValue = dfs.FileInfo.DeleteValueFloat

        n_items = len(item_numbers)
        data_list = []

        for item in range(n_items):
            # Initialize an empty data block
            data = np.ndarray(shape=(nt, xNum), dtype=float)
            data_list.append(data)

        t = []
        startTime = dfs.FileInfo.TimeAxis.StartDateTime
        for it in range(dfs.FileInfo.TimeAxis.NumberOfTimeSteps):
            for item in range(n_items):

                itemdata = dfs.ReadItemTimeStep(item_numbers[item] + 1, it)

                src = itemdata.Data
                d = to_numpy(src)

                d[d == deleteValue] = np.nan
                data_list[item][it, :] = d

            t.append(
                startTime.AddSeconds(itemdata.Time).ToString("yyyy-MM-dd HH:mm:ss")
            )

        time = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in t]
        names = []
        for item in range(n_items):
            name = dfs.ItemInfo[item].Name
            names.append(name)

        dfs.Close()
        return Dataset(data_list, time, names)

    def write(self, filename, data):
        """
        Function: write to a pre-created dfs1 file.

        filename:
            full path and filename to existing dfs1 file

        data:
            list of matrices. len(data) must equal the number of items in the dfs2.
            Each matrix must be of dimension time, x

        usage:
            write(filename, data) where  data(nt, x)

        Returns:
            Nothing

        """

        # Open the dfs file for writing
        dfs = DfsFileFactory.filenameOpenEdit(filename)

        # Determine the size of the grid
        number_x = dfs.SpatialAxis.XCount
        n_time_steps = dfs.FileInfo.TimeAxis.NumberOfTimeSteps
        n_items = safe_length(dfs.ItemInfo)

        deletevalue = -1e-035

        if not all(np.shape(d)[0] == n_time_steps for d in data):
            raise Warning(
                "ERROR data matrices in the time dimension do not all match in the data list. "
                "Data is list of matices [t, x]"
            )
        if not all(np.shape(d)[1] == number_x for d in data):
            raise Warning(
                "ERROR data matrices in the X dimension do not all match in the data list. "
                "Data is list of matices [t, x]"
            )

        if not len(data) == n_items:
            raise Warning(
                "The number of matrices in data do not match the number of items in the dfs1 file."
            )

        for i in range(n_time_steps):
            for item in range(n_items):
                d = data[item][:, i]
                d[np.isnan(d)] = deletevalue
                darray = Array[System.Single](np.array(d.reshape(d.size, 1)[:, 0]))
                dfs.WriteItemTimeStepNext(0, darray)

        dfs.Close()

    def create(
        self,
        filename,
        data,
        start_time=None,
        dt=1,
        length_x=1,
        x0=0,
        coordinate=None,
        timeseries_unit=TimeStep.SECOND,
        variable_type=None,
        unit=None,
        names=None,
        title=None,
    ):
        """
        Creates a dfs1 file

        filename:
            Location to write the dfs1 file
        data:
            list of matrices, one for each item. Matrix dimension: x, time
        start_time:
            start date of type datetime.
        timeseries_unit:
            TimeStep default TimeStep.SECOND
        dt:
            The time step (double based on the timeseries_unit). Therefore dt of 5.5 with timeseries_unit of minutes
            means 5 mins and 30 seconds.
        variable_type:
            Array integers corresponding to a variable types (ie. Water Level). Use dfsutil type_list
            to figure out the integer corresponding to the variable.
        unit:
            Array integers corresponding to the unit corresponding to the variable types The unit (meters, seconds),
            use dfsutil unit_list to figure out the corresponding unit for the variable.
        coordinate:
            ['UTM-33', 12.4387, 55.2257, 327]  for UTM, Long, Lat, North to Y orientation. Note: long, lat in decimal degrees
            OR
            [TODO: Support not Local Coordinates ...]
        x0:
            Lower right position
        length_x:
            length of each grid in the x direction (meters)
        names:
            array of names (ie. array of strings). (can be blank)
        title:
            title of the dfs2 file (can be blank)

        """

        if title is None:
            title = ""

        n_time_steps = np.shape(data[0])[0]
        number_x = np.shape(data[0])[1]
        n_items = len(data)

        if start_time is None:
            start_time = datetime.now()

        if coordinate is None:
            coordinate = ["LONG/LAT", 0, 0, 0]

        if names is None:
            names = [f"Item {i+1}" for i in range(n_items)]

        if variable_type is None:
            variable_type = [999] * n_items

        if unit is None:
            unit = [0] * n_items

        if not all(np.shape(d)[0] == n_time_steps for d in data):
            raise Warning(
                "ERROR data matrices in the time dimension do not all match in the data list. "
                "Data is list of matices [t, x]"
            )
        if not all(np.shape(d)[1] == number_x for d in data):
            raise Warning(
                "ERROR data matrices in the X dimension do not all match in the data list. "
                "Data is list of matices [t, x]"
            )

        if len(names) != n_items:
            raise Warning(
                "names must be an array of strings with the same number as matrices in data list"
            )

        if len(variable_type) != n_items or not all(
            isinstance(item, int) and 0 <= item < 1e15 for item in variable_type
        ):
            raise Warning(
                "type if specified must be an array of integers (enuType) with the same number of "
                "elements as data columns"
            )

        if len(unit) != n_items or not all(
            isinstance(item, int) and 0 <= item < 1e15 for item in unit
        ):
            raise Warning(
                "unit if specified must be an array of integers (enuType) with the same number of "
                "elements as data columns"
            )

        if not type(start_time) is datetime:
            raise Warning("start_time must be of type datetime ")

        # if not isinstance(timeseries_unit, int):
        #    raise Warning("timeseries_unit must be an integer. timeseries_unit: second=1400, minute=1401, hour=1402, "
        #                  "day=1403, month=1405, year= 1404See dfsutil options for help ")

        system_start_time = System.DateTime(
            start_time.year,
            start_time.month,
            start_time.day,
            start_time.hour,
            start_time.minute,
            start_time.second,
        )

        # Create an empty dfs1 file object
        factory = DfsFactory()
        builder = Dfs1Builder.Create(title, "mikeio", 0)

        # Set up the header
        builder.SetDataType(0)
        builder.SetGeographicalProjection(
            factory.CreateProjectionGeoOrigin(
                coordinate[0], coordinate[1], coordinate[2], coordinate[3]
            )
        )
        builder.SetTemporalAxis(
            factory.CreateTemporalEqCalendarAxis(
                timeseries_unit, system_start_time, 0, dt
            )
        )
        builder.SetSpatialAxis(
            factory.CreateAxisEqD1(eumUnit.eumUmeter, number_x, x0, length_x)
        )

        for i in range(n_items):
            builder.AddDynamicItem(
                names[i],
                eumQuantity.Create(variable_type[i], unit[i]),
                DfsSimpleType.Float,
                DataValueType.Instantaneous,
            )

        try:
            builder.CreateFile(filename)
        except IOError:
            print("cannot create dfs2 file: ", filename)

        dfs = builder.GetFile()
        deletevalue = dfs.FileInfo.DeleteValueFloat  # -1.0000000031710769e-30

        for i in range(n_time_steps):
            for item in range(n_items):
                d = data[item][i, :]
                d[np.isnan(d)] = deletevalue
                darray = Array[System.Single](np.array(d.reshape(d.size, 1)[:, 0]))
                dfs.WriteItemTimeStepNext(0, darray)

        dfs.Close()
